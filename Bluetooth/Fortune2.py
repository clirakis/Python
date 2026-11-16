from pynput import keyboard
buttons = {
'l': 'A',
'k': 'B',
'u': 'Y',
'y': 'X',
}
state = {button: False for button in buttons.values()}

def on_press(key):
    char = getattr(key, 'char', None)
    button = buttons.get(char)

    if button and not state[button]:
        state[button] = True
        print(f"{button} PRESSED")

def on_release(key):
    char = getattr(key, 'char', None)
    button = buttons.get(char)
    if button and state[button]:
        state[button] = False
        print(f"{button} RELEASED")

with keyboard.Listener(
        on_press=on_press,
        on_release=on_release
) as listener:
    listener.join()
