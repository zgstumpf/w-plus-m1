from pynput import mouse, keyboard

import json
import signal
import sys

# TODO:
# keep track of how long each button is held down for
# store this in persistent file, different file for each script session

keyData = {}
"""
key (str): elapsed time (float)
"""

def on_click(x, y, button, pressed):
    if pressed and button == mouse.Button.left:
        print('M1 pressed')
    elif not pressed:
        print(button, 'released')

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))

# signum and frame are required arguments for signal handler callback function
def save_data(signum, frame):
    print('persist data')
    # with open("data.json", "w") as file:
    #     json.dump(data, file)
    sys.exit(0)

# Register signal handlers to save data on Ctrl+C or termination
signal.signal(signal.SIGINT, save_data)  # Ctrl+C
signal.signal(signal.SIGTERM, save_data) # Termination signal

keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
mouse_listener = mouse.Listener(on_click=on_click)

# Start threads
keyboard_listener.start()
mouse_listener.start()

# Keep threads running until program is terminated
# These lines must be at end of file
keyboard_listener.join()
mouse_listener.join()