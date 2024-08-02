from pynput import mouse, keyboard

import json
import signal
import sys
import time
import pprint
from typing import Dict

# TODO:
# keep track of how long each button is held down for
# store this in persistent file, different file for each script session

class Key:
    def __init__(self, key: str):
        self.key = key
        self.lastPressTimeWithoutRelease = time.time()
        self.totalTime = 0

    def __repr__(self):
        return f"Key(key='{self.key}', lastPressTimeWithoutRelease={self.lastPressTimeWithoutRelease}, totalTime={self.totalTime})"

    def regenerateLastPressTime(self):
        self.lastPressTimeWithoutRelease = time.time()

    def clearLastPressTime(self):
        self.lastPressTimeWithoutRelease = None

    def is_unreleased(self):
        """
        Returns True if key is currently being held down, False otherwise.
        """
        if self.lastPressTimeWithoutRelease is not None:
            return True
        else:
            return False


class Session:
    keyData: Dict[str, Key] = {}
    """
    key (str): Key()
    """

    @classmethod
    def register_key_press(cls, key: str):
        key = cls.normalize_key(key)

        if key not in cls.keyData:
            cls.keyData[key] = Key(key)
        else:
            keyInstance = cls.keyData[key]
            # When a key is held down, it constantly sends a stream of register_key_press actions
            # Do not execute rest of this code if key is being held down
            if keyInstance.is_unreleased():
                return

            keyInstance.regenerateLastPressTime()

    @classmethod
    def register_key_release(cls, key: str):
        key = cls.normalize_key(key)

        # key should always be in keyData, since key can't be released without being pressed first
        keyInstance = cls.keyData[key]

        keyInstance.totalTime = keyInstance.totalTime + (time.time() - keyInstance.lastPressTimeWithoutRelease)

        keyInstance.clearLastPressTime()


    @classmethod
    def normalize_key(cls, key):
        # key may be <str> or other pynput class such as <keyboard._darwin.KeyCode>
        # Convert input to str
        key = str(key)

        # Sometimes pynput str conversion produces a string like "'a'" (2 single quotation marks)
        # To keep things simple, remove all non alphanumeric characters
        chars = list(key)
        chars = [char for char in chars if char.isalnum()]

        # Finally, convert to string
        key = "".join(chars)

        return key




def on_click(x, y, button, pressed):
    if pressed and button == mouse.Button.left:
        print('M1 pressed')
        session.register_key_press(button)
    elif not pressed:
        session.register_key_release(button)
        print(button, 'released')

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
        session.register_key_press(key.char)
    except AttributeError:
        print('special key {0} pressed'.format(
            key))
        session.register_key_press(key)

def on_release(key):
    # For some reason this does not need try except as in on_press()
    print('{0} released'.format(
        key))
    session.register_key_release(key)

# signum and frame are required arguments for signal handler callback function
def save_data(signum, frame):
    print('persist data')
    pprint.pprint(session.keyData)
    # with open("data.json", "w") as file:
    #     json.dump(data, file)
    sys.exit(0)


if __name__ == "__main__":
    # Register signal handlers to save data on Ctrl+C or termination
    signal.signal(signal.SIGINT, save_data)  # Ctrl+C
    signal.signal(signal.SIGTERM, save_data) # Termination signal

    session = Session()

    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    mouse_listener = mouse.Listener(on_click=on_click)

    # Start threads
    keyboard_listener.start()
    mouse_listener.start()

    # Keep threads running until program is terminated
    # These lines must be at end of file
    keyboard_listener.join()
    mouse_listener.join()




# Bugs to think about pull request
# 1. Stupid str conversion for some pynput types - converts to "'a'" instead of "a"