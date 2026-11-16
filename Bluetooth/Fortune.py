from pynput import keyboard
from time import monotonic
start = monotonic()
def log_event(action, key):
    elapsed = monotonic() - start
    if isinstance(key, keyboard.KeyCode):
        name = repr(key.char)
    else:
        name = str(key)
    print(f"{elapsed:8.3f}  {action:7}  {name}", flush=True)
    
def on_press(key):
    log_event("DOWN", key)
    
def on_release(key):
    log_event("UP", key)
    
print("Listening for keyboard events...")
print("Press Ctrl+C to stop.")
with keyboard.Listener(
    on_press=on_press,
    on_release=on_release
) as listener:
    listener.join()
