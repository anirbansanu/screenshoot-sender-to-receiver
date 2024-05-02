import socket
import datetime

class ScreenshotReceiver:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def connect(self):
        self.receiver_socket.connect((self.host, self.port))

    def request_screenshot(self):
        self.receiver_socket.sendall(b'take_screenshot')

    def receive_screenshot(self):
        data_size = int.from_bytes(self.receiver_socket.recv(4), byteorder='big')
        screenshot_bytes = b""
        chunk_size = 1024
        remaining_size = data_size
        while remaining_size > 0:
            data = self.receiver_socket.recv(min(chunk_size, remaining_size))
            screenshot_bytes += data
            remaining_size -= len(data)
        return screenshot_bytes

    def save_screenshot(self, screenshot_bytes):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        filename = f"{timestamp}_screenshot.png"
        with open(filename, 'wb') as f:
            f.write(screenshot_bytes)
        print(f"Screenshot received and saved as '{filename}'")
        return filename

    def run(self):
        while True:
            user_input = input("Enter 's' to request a screenshot, or 'exit' or 'q' to quit: ")

            if user_input.lower() in ('exit', 'q'):
                self.close()
                break
            
            elif user_input.lower() == 's':
                self.request_screenshot()
                screenshot_data = self.receive_screenshot()
                self.save_screenshot(screenshot_data)

    def close(self):
        self.receiver_socket.sendall(b'exit')
        self.receiver_socket.close()

if __name__ == "__main__":
    try:
        receiver = ScreenshotReceiver()
        receiver.run()

    except Exception as e:
        print(f"Error: {e}")
