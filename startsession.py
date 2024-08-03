from pynput import mouse, keyboard

import csv
import signal
import sys
import os
import time
from typing import Dict

from utils import print_wm1_intro


class Key:
    """
    A data record for a specific key or mouse click.

    - key (str): String representation of the key

    - lastPressTimeWithoutRelease (float): While the key is being held down, this is the time when it was pressed to start.
    Used to calculate how long the key was held down for once it is released.
    Represented as time in seconds since the Epoch.

    - totalTime (float): The total elapsed time in seconds the key has been held down for during the session.

    Even if a key is pressed and immediately released, the code still detects an elapsed time between those two events.
    """
    def __init__(self, key: str):
        """
        Initialize a new Key object. This should be called when a key is pressed for the first time in a session.
        """
        self.key = key
        self.lastPressTimeWithoutRelease = time.time()
        self.totalTime = 0. # make float


    def __repr__(self):
        """
        Converts a Key instance in memory to a readable format.
        """
        return f"Key(key='{self.key}', lastPressTimeWithoutRelease={self.lastPressTimeWithoutRelease}, totalTime={self.totalTime}s)"


    def regenerate_last_press_time(self):
        """
        Sets the Key's lastPressTimeWithoutRelease to the current time in seconds since the Epoch.

        This function should be called when an already initialized Key is pressed.
        """
        self.lastPressTimeWithoutRelease = time.time()


    def clear_last_press_time(self):
        """
        Sets the Key's lastPressTimeWithoutRelease to None, signifying that the key has been released and is not being held down.

        Any calculations using lastPressTimeWithoutRelease must be performed before calling this method.
        """
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
    """
    Represents a monitoring session capable of storing a user's keyboard and mouse inputs in memory.
    When the session ends, data is saved persistently for further analysis.
    """
    name: str

    keyData: Dict[str, Key] = {}
    """
    Maps the string representation of a key to its Key instance tracked by the Session.

    Example: {'a': Key(key='a', ...)}
    """


    @classmethod
    def prompt_name(cls):
        """
        Prompts user for a name for the session.
        """
        print('When the session ends, its data will be saved to a file.')
        print('You can give this session a name which will carry over to the filename.')
        print('The current date will automatically be added to the file name.')

        name = input('Enter session name, or press enter to skip: ')
        return name


    @classmethod
    def set_name(cls, name: str):
        """
        Sets the name of the session.
        """
        timestamp = time.strftime("%d%b%Y_%H:%M:%S", time.localtime())

        if name:
            # set name to user-defined name + underscore + timestamp
            name += '_' + timestamp
        else:
            # set name to just timestamp
            name = timestamp

        cls.name = name


    @classmethod
    def register_key_press(cls, key: str):
        """
        Stores key press in memory. If key is already being tracked, resets the time it was last pressed.
        """
        key = cls.normalize_key(key)
        print(key, 'pressed')
        if key not in cls.keyData:
            cls.keyData[key] = Key(key)
        else:
            keyInstance = cls.keyData[key]
            # When a key is held down, it constantly sends a stream of register_key_press actions
            # Do not execute rest of this code if key is being held down
            if keyInstance.is_unreleased():
                return

            keyInstance.regenerate_last_press_time()


    @classmethod
    def register_key_release(cls, key: str):
        """
        Modifies key data in memory, updating the total time the key has been held down for and noting that the
        key is not being held down.
        """
        key = cls.normalize_key(key)
        print(key, 'released')
        # key should always be in keyData, since key can't be released without being pressed first,
        # and pressing stores the key in keyData.
        keyInstance = cls.keyData[key]

        timeKeyWasHeldDown = time.time() - keyInstance.lastPressTimeWithoutRelease
        keyInstance.totalTime += timeKeyWasHeldDown

        keyInstance.clear_last_press_time()


    @classmethod
    def normalize_key(cls, key):
        """
        Converts a key object to a string.

        The specific key object may be different for when a key was pressed vs. released, making this function necessary.
        """
        # key may be <str> or other pynput class such as <keyboard._darwin.KeyCode>
        # Convert input to string
        key = str(key)

        # Sometimes converting a pynput object to a string produces a string like "'a'" (Note the 2 single quotation marks)
        # Remove these single quotations if they exist, making sure to not remove the single quotation in a string such as
        # "'", which means the user pressed the single quotation key
        chars = list(key)
        print(f"{chars=}")
        if len(chars) >= 3 and chars[0] == "'" and chars[-1] == "'":
            chars = chars[1:-1]

        # Fix bug: when ' is pressed, chars is ["'"] (correct), when ' released chars is ['"', "'", '"'] (incorrect)
        if chars == ['"', "'", '"']:
            chars = ["'"]

        # Convert back to string
        key = "".join(chars)

        # Lowercase string. This fixes bug where:
        # 1. key 'a' is held down
        # 2. key 'Keyshift' is held down, making anything pressed next capitalized
        # 3. key 'a' is released, but it is registered as 'A'.
        # So, 'A' was registered as released, but it was never pressed, leading to bug.
        key = key.lower()

        return key


    @classmethod
    def remove_ctrl_c_keys(cls):
        """
        If the program is terminated with ctrl + c, the ctrl and c key are the last keys added to keyData.
        This function makes sure those presses do not affect the data.
        """

        # The program terminates before detecting the keys ctrl and c being released.
        # If 'c' is already in keyData, the final press is detected as pressed but never detected as released,
        # so it has no effect on the data.
        # If 'c' is NOT already in keyData, the final press adds it to keyData with a totalTime of 0.
        # In this case, it should be removed.
        if 'c' in cls.keyData:
            cKeyInstance = cls.keyData['c']
            if cKeyInstance.totalTime == 0:
                del cls.keyData['c']

        # Apply same concept to 'ctrl' key. In the code, it is represented as 'keyctrl' (after being lowercased).
        if 'keyctrl' in cls.keyData:
            ctrlKeyInstance = cls.keyData['keyctrl']
            if ctrlKeyInstance.totalTime == 0:
                del cls.keyData['keyctrl']


    @classmethod
    def to_csv(cls):
        """
        Cleans up the session data and stores it in a CSV file. Returns absolute filepath of final CSV file.
        """
        cls.remove_ctrl_c_keys()

        # keyData dictionary stores key data repetitively. Example: {'a': Key(key='a', ...}
        # This enables quick access during runtime, but all the meaningful data is in the dictionary values
        data = list(cls.keyData.values())

        # Sort keys with most total time first. This ensures bars are sorted when data is graphed.
        data.sort(key= lambda keyInstance: keyInstance.totalTime, reverse=True)

        # Remove this property because it is not useful for data analysis and only used during runtime to calculate totalTime
        for object in data:
            del object.lastPressTimeWithoutRelease

        # Gets absolute path of directory of this script
        project_directory = os.path.dirname(os.path.abspath(__file__))

        # Plan to store data in 'data' directory within this project directory
        target_directory = os.path.join(project_directory, 'data')
        os.makedirs(target_directory, exist_ok=True)

        filename = f"{cls.name}.csv"
        filepath = os.path.join(target_directory, filename)

        # Write session to CSV file
        with open(filepath, 'w', newline='') as file:
            writer = csv.writer(file)

            # Header row
            writer.writerow(['key', 'totalTime'])

            # Data rows
            for object in data:
                writer.writerow([object.key, object.totalTime])

        return filepath


def on_click(_, __, button, pressed):
    """
    Fires when a mouse button is pressed down or released.
    """
    if pressed:
        session.register_key_press(button)
    else:
        # released
        session.register_key_release(button)


def on_press(key):
    """
    Fires when a keyboard key is pressed down.
    """
    try:
        session.register_key_press(key.char)
    except AttributeError:
        # special keys dont have char attribute
        session.register_key_press(key)


def on_release(key):
    """
    Fires when a keyboard key is released.
    """
    # For some reason this does not need try except as in on_press()
    session.register_key_release(key)


def save_data(signum, frame):
    """
    Saves data from the current session to persistent storage and ends the program.
    """
    # signum and frame are required arguments for signal handler callback function,
    # even if they are never used. They are put here so code editor doesn't
    # complain about unaccessed parameters
    signum, frame

    import pprint
    pprint.pprint(session.keyData)
    filepath = session.to_csv()
    print(f'Data saved at {filepath}')

    # End the program
    sys.exit(0)


if __name__ == "__main__":
    # Register signal handlers to save data on Ctrl+C or termination
    signal.signal(signal.SIGINT, save_data)  # Ctrl+C
    signal.signal(signal.SIGTERM, save_data) # Termination signal

    print_wm1_intro()
    print("-> You are about to start an input tracker session.\n")

    # Prepare session to store keyboard and mouse inputs in memory
    session = Session()
    name = session.prompt_name()
    session.set_name(name)

    # Prepare input listeners
    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    mouse_listener = mouse.Listener(on_click=on_click)

    # TODO: put try/except here to save data if program crashes???
    # Start threads for input listeners, meaning they will begin listening for inputs
    print('Session started. Tracking keyboard and mouse inputs... Ctrl + c to stop.')
    keyboard_listener.start()
    mouse_listener.start()

    # Keep threads running until program is terminated
    # These lines must be at end of file
    keyboard_listener.join()
    mouse_listener.join()




# Bugs to think about pull request
# 1. Stupid str conversion for some pynput types - converts to "'a'" instead of "a"