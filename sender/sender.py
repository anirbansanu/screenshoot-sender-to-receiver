import socket
from PIL import ImageGrab
import io

class ScreenshotSender:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.sender_socket = None

    def establish_connection(self):
        self.sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sender_socket.bind((self.host, self.port))
        self.sender_socket.listen(1)
        print("Sender waiting for connection...")

    def send_screenshot(self):
        conn, addr = self.sender_socket.accept()
        print(f"Connected to {addr}")

        while True:
            command = conn.recv(1024).decode()

            if command.lower() == 'take_screenshot':
                screenshot = ImageGrab.grab()
                with io.BytesIO() as buffer:
                    screenshot.save(buffer, format="PNG")
                    screenshot_bytes = buffer.getvalue()

                conn.sendall(len(screenshot_bytes).to_bytes(4, byteorder='big'))

                chunk_size = 1024
                for i in range(0, len(screenshot_bytes), chunk_size):
                    conn.sendall(screenshot_bytes[i:i + chunk_size])

                print("Screenshot sent successfully")

            elif command.lower() == 'exit':
                self.sender_socket.close()
                print("Connection Closed, Exiting...")
                break

    def run(self):
        try:
            self.establish_connection()
            self.send_screenshot()

        except Exception as e:
            print(f"Error: {e}")

        finally:
            if self.sender_socket:
                self.sender_socket.close()

if __name__ == "__main__":
    sender = ScreenshotSender()
    sender.run()
