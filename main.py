from pynput import mouse, keyboard

import json
import signal
import sys

data = []

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

def save_data():
    print('persist data')
    # with open("data.json", "w") as file:
    #     json.dump(data, file)

def handle_exit(signum, frame):
    print("Signal received, saving data...")
    save_data()
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, handle_exit)  # Handle Ctrl+C
signal.signal(signal.SIGTERM, handle_exit) # Handle termination signal


keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
mouse_listener = mouse.Listener(on_click=on_click)

# Start threads
keyboard_listener.start()
mouse_listener.start()

# keep track of how long each button is held down for
# store this in persistent file, different file for each script session

# with open("data.json", "w") as file:
#     json.dump(data, file)

# Keep threads running until program is terminated with ctrl + c
# These lines must be at end of file
keyboard_listener.join()
mouse_listener.join()