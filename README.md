# Educational Keylogger - Learning Project

<div align="center">

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Purpose](https://img.shields.io/badge/Purpose-Educational-orange.svg)

**A feature-rich keylogger implementation designed for learning programming concepts**

</div>

## ⚠️ Important Disclaimer

> **THIS SOFTWARE IS FOR EDUCATIONAL PURPOSES ONLY**
> 
> - 🚫 **Do not use on computers you don't own**
> - 🚫 **Do not use without explicit permission**
> - 🚫 **Do not use for malicious activities**
> - ✅ **Only use for learning and research**
> 
> The creators are not responsible for any misuse of this software. Use responsibly and ethically.

## 📚 Learning Objectives

This project demonstrates real-world implementations of:

- **Event-driven programming** with keyboard listeners
- **File I/O operations** and log management
- **Object-oriented design** patterns
- **Threading and synchronization**
- **Data structures** and analytics
- **Performance optimization** techniques
- **Error handling** and resource management

## 🛠️ Features

### Core Functionality
- ✅ Real-time keyboard event capture
- ✅ Special key normalization (Space, Enter, Tab, etc.)
- ✅ Log file rotation with size limits
- ✅ Buffered writing for performance
- ✅ Session analytics and statistics

### Educational Features
- 📊 **Key frequency analysis**
- ⏱️ **Typing speed metrics**
- 📈 **Session duration tracking**
- 🔄 **Automatic file management**
- 🛡️ **Proper resource cleanup**

## 🚀 Quick Start

### Prerequisites
- Python 3.6 or higher
- pynput library

### Installation
```bash
# Clone or download the script
# Install required dependency
pip install pynput

# Run the educational keylogger
python educational_keylogger.py

# Press ESC key to stop logging and view analytics


educational_keylogger/
│
├── educational_keylogger.py  # Main script
├── educational_logs/         # Log directory (auto-created)
│   └── key_log_YYYY-MM-DD_HH-MM-SS.txt
└── README.md                # This file

Keyboard Event → Normalize Key → Buffer → Batch Write → Log File
       ↓
 Analytics → Statistics → Session Report
