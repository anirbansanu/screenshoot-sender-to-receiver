import socket
import datetime

def receive_screenshot(host='127.0.0.1', port=12345):
    try:
        # Establish a connection to the sender
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as receiver_socket:
            receiver_socket.connect((host, port))
            
            while True:
                # Prompt user for input
                user_input = input("Enter 's' to request a screenshot, or 'exit' or 'q' to quit: ")

                if user_input.lower() == 'exit' or user_input.lower() == 'q':
                    receiver_socket.sendall(b'exit')
                    break
                
                elif user_input.lower() == 's':
                    # Send request to sender for screenshot
                    receiver_socket.sendall(b'take_screenshot')

                    # Receive the size of the screenshot data
                    data_size = int.from_bytes(receiver_socket.recv(4), byteorder='big')

                    # Receive the screenshot data in chunks
                    screenshot_bytes = b""
                    chunk_size = 1024
                    remaining_size = data_size
                    while remaining_size > 0:
                        data = receiver_socket.recv(min(chunk_size, remaining_size))
                        screenshot_bytes += data
                        remaining_size -= len(data)
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
                    filename = f"{timestamp}_screenshot.png"
                    # Save the received screenshot data as a PNG file
                    with open(filename, 'wb') as f:
                        f.write(screenshot_bytes)

                    print(f"Screenshot received and saved as '{filename}'")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    receive_screenshot()
