# Skid Larps
Skid Larps RAT (Remote Access Trojan) is a Python-based application that demonstrates the integration of multiple libraries for GUI interaction, multimedia processing, Discord integration, and system utilities. This project is intended for learning, experimentation, and understanding how different Python modules can work together in a multi-threaded, asynchronous, and event-driven environment.
---
**# Table of Contents**
1. Overview
2. Features
3. Requirements
4. Installation
5. Usage
6. Modules and Imports
7. Project Structure
8. Contributing
9. License
---
**# Overview**
Skid Larps RAT serves as a sandbox-style project that combines graphical user interfaces, audio recording, screen capture, image processing, Discord bot communication, and basic system-level interactions. It also includes basic [!] functionality for remote-style command execution, primarily to demonstrate event handling, message parsing, and task execution logic.
The project showcases the following concepts:
- Multi-threaded GUI applications using tkinter
- Asynchronous and non-blocking operations with asyncio
- Multimedia processing with sounddevice, OpenCV, and PIL
- External process execution and OS interaction using subprocess and os
- Discord bot integration through discord.py
- Utility functions such as math operations, random value generation, and temporary file handling
This project is ideal for Python developers who want to explore how multiple libraries can be combined into a single cohesive application while maintaining responsiveness and modularity.
---
**# Features**
- Graphical User Interface 
  Built using tkinter, providing buttons, menus, status displays, and interactive elements that update dynamically without freezing the application.

- Discord Integration
  Uses discord.py to connect to Discord servers, send messages, receive commands, and trigger internal application functions through bot events.

- Audio Recording
  Supports recording microphone or system audio using sounddevice and saving recordings to WAV format with scipy.io.wavfile.

- Screen Capture and Image Processing
  Captures screenshots using PIL.ImageGrab and processes images using OpenCV for resizing, filtering, or analysis.

- Multi-threading and Async Support
  Background tasks run in separate threads or asynchronous loops to ensure the GUI remains responsive during long operations.

- Randomization Utilities
  Includes random number and value generation for testing, simulations, or experimental logic.

- System Process Management
  Uses subprocess and os to execute system commands, manage files, and interact with the operating system environment.
---
**# Requirements**
- Python version: 3.13 or higher
- Operating System: Windows 11 recommended (for full feature support)
Required Python packages:
pip install tkinter pillow opencv-python discord.py sounddevice scipy
---
**# Installation**
1. Install Python 3.13 or newer from the official Python website.
2. Ensure Python is added to your system PATH.
3. Install the required dependencies using pip.
4. Download or clone the Skid Larps project files.
5. Configure any required settings such as Discord bot tokens inside the configuration files or source code.
---
**# Usage**
1. HAve Target run the main.py script in coding sys terminal using py 3.13+
2. Interact with [!] cmds in discord to trigger audio recording, screen capture, utility functions, & much more.
3. If Discord integration is enabled, start the bot and issue supported commands from a Discord server.
4. Monitor logs and console output for task execution status and debugging information.
Note: This project is real RAT so use at own risk...
---
**# Modules and Imports**
Commonly used modules in this project include:
- tkinter (GUI framework)
- asyncio (asynchronous task management)
- threading (multi-threaded execution)
- sounddevice (audio input/output)
- scipy.io.wavfile (audio file handling)
- cv2 / OpenCV (image processing)
- PIL / Pillow (image capture and manipulation)
- discord.py (Discord bot integration)
- subprocess (external command execution)
- os (operating system utilities)
- math (mathematical operations)
- random (randomized values)
- tempfile (temporary file handling)
---
**# Project Structure**
project layout:
/skid-larps
│
├── main.py              Main app
└── README.txt           Project documentation / req.
---
**# License**
This project is provided for Skid Larp members & more, but i dont any problems that occur while using the tool.
