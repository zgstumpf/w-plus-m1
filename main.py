from pynput import mouse, keyboard

def on_click(x, y, button, pressed):
    if pressed and button == mouse.Button.left:
        print('M1 pressed')


def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))


keyboard_listener = keyboard.Listener(on_press=on_press)
mouse_listener = mouse.Listener(on_click=on_click)

# Start threads
keyboard_listener.start()
mouse_listener.start()

# Keep threads running until program is terminated with ctrl + c
keyboard_listener.join()
mouse_listener.join()