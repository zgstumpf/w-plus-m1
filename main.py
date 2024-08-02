from pynput import mouse, keyboard

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


keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
mouse_listener = mouse.Listener(on_click=on_click)

# Start threads
keyboard_listener.start()
mouse_listener.start()

# Keep threads running until program is terminated with ctrl + c
keyboard_listener.join()
mouse_listener.join()

# keep track of how long each button is held down for
# store this in persistent file, different file for each script session