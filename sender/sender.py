import socket
from PIL import ImageGrab
import io

def send_screenshot(host='127.0.0.1', port=12345):
    try:
        # Establish a connection to the receiver
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sender_socket:
            sender_socket.bind((host, port))
            sender_socket.listen(1)
            print("Sender waiting for connection...")

            conn, addr = sender_socket.accept()
            print(f"Connected to {addr}")

            while True:
                # Wait for command from receiver
                command = conn.recv(1024).decode()

                if command.lower() == 'take_screenshot':
                    # Capture the screenshot using Pillow (PIL)
                    screenshot = ImageGrab.grab()

                    # Convert the screenshot to PNG format
                    with io.BytesIO() as buffer:
                        screenshot.save(buffer, format="PNG")
                        screenshot_bytes = buffer.getvalue()

                    # Send the size of the screenshot data
                    conn.sendall(len(screenshot_bytes).to_bytes(4, byteorder='big'))

                    # Send the screenshot data in chunks
                    chunk_size = 1024
                    for i in range(0, len(screenshot_bytes), chunk_size):
                        conn.sendall(screenshot_bytes[i:i + chunk_size])

                    print("Screenshot sent successfully")

                elif command.lower() == 'exit':
                    print("Exiting...")
                    break

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    send_screenshot()
