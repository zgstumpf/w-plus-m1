from pynput import mouse, keyboard

import json
import signal
import sys
import time

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


class Session:
    keyData = {}
    """
    key (str): Key()
    """

    @classmethod
    def register_key_press(cls, key: str):
        key = cls.normalize_key(key)
        if key not in cls.keyData:
            cls.keyData[key] = Key(key)
            print(cls.keyData)
        else:
            cls.keyData[key].regenerateLastPressTime()
        print(key, 'registered press')

    @classmethod
    def register_key_release(cls, key: str):
        # on release, key is not a simple str, it is something like <class 'pynput.keyboard._darwin.KeyCode'>
        print('key in register for release:', key, type(key), str(key))
        print('normal string stdout', 'a')
        key = cls.normalize_key(key)
        print('key after normalizing', key, type(key))
        print(cls.keyData)
        print('keyData key type', type(list(cls.keyData.keys())[0]))
        if key in cls.keyData:
            print('key in keyData')
        else:
            print('key not in keyData')
        key = cls.keyData[key] # BUG: KeyError: "'a'"
        key.totalTime = key.totalTime + (time.time() - key.lastPressTimeWithoutRelease)
        key.clearLastPressTime()
        print(key, 'registered release')


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
        session.normalize_key(key.char)
        session.register_key_press(key.char)
    except AttributeError:
        print('special key {0} pressed'.format(
            key))
        session.register_key_press(key)

def on_release(key):
    # ???? does this need try except key.char like on_press?
    print('{0} released'.format(
        key))
    session.register_key_release(key)

# signum and frame are required arguments for signal handler callback function
def save_data(signum, frame):
    print('persist data')
    print(session.keyData)
    # with open("data.json", "w") as file:
    #     json.dump(data, file)
    sys.exit(0)

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