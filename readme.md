# Sender and Receiver Documentation

## Introduction
This documentation provides an overview of the functionality and usage of `sender.py` and `receiver.py`, Python scripts designed for capturing and transmitting screenshots over a socket connection.

## `sender.py`

### Overview
`sender.py` captures screenshots and sends them to a connected receiver script upon request.

### Usage
1. Run `sender.py` on the sender machine.
2. Ensure the receiver script (`receiver.py`) is running on the receiver machine.
3. Wait for commands from the receiver script to capture and send screenshots.

### Dependencies
- `socket`: Standard Python library for socket communication.
- `PIL` (Python Imaging Library): Required for capturing and saving screenshots.

### Code Structure
```python
import socket
from PIL import ImageGrab
import io

def send_screenshot(host='127.0.0.1', port=12345):
    try:
        # Code implementation
        pass

if __name__ == "__main__":
    send_screenshot()
```

### Functionality
- Establishes a socket connection to listen for commands.
- Captures the screen using PIL.
- Converts the screenshot to PNG format.
- Sends the screenshot data in chunks over the socket connection.

## `receiver.py`

### Overview


`receiver.py` receives screenshots from sender.py and saves them to disk.

### Usage
1. Run receiver.py on the receiver machine.
2. Ensure sender.py is running on the sender machine.
3. Enter commands in receiver.py to request screenshots or exit the program.

### Dependencies

socket: Standard Python library for socket communication.
PIL (Python Imaging Library): Optional for displaying screenshots.
### Code Structure
```python
import socket
from PIL import ImageGrab
import io

def receive_screenshot(host='127.0.0.1', port=12345):
    try:
        # Code implementation goes here
        pass

if __name__ == "__main__":
    receive_screenshot()
```

###  Functionality
- Establishes a socket connection to communicate with sender.py.
- Sends commands to request screenshots or exit.
- Receives screenshot data and saves it with a timestamped filename.
###  Conclusion
Together, sender.py and receiver.py provide a solution for capturing and transmitting screenshots between machines over a socket connection.
