import socket
import pyautogui
import os
import datetime

def take_screenshot():
    screenshot = pyautogui.screenshot()
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y-%H:%M:%S")
    filename = f"screenshot_{timestamp}.png"
    screenshot.save(filename)
    print("Screenshot taken")
    return filename

def send_screenshot(conn, filename, buffer_size):
    try:
        with open(filename, "rb") as f:
            while True:
                data = f.read(buffer_size)
                if not data:
                    break
                conn.sendall(data)
        print("Screenshot sent")
        ack = conn.recv(1024)  # Wait for receiver's acknowledgment
        if ack == b"Screenshot received":
            print("Receiver acknowledged receipt of the screenshot.")
        else:
            print("Receiver did not acknowledge receipt of the screenshot.")
    except ConnectionResetError:
        print("Connection reset by peer. Retrying...")

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 3005))  # Bind to all interfaces
    s.listen()

    print("Waiting for connection...")
    conn, addr = s.accept()
    print(f"Connected to {addr}")

    while True:
        request = conn.recv(1024).decode()
        if request == "send_screenshot":
            filename = take_screenshot()
            buffer_size = 4096  # Specify the buffer size in bytes
            send_screenshot(conn, filename, buffer_size)
            os.remove(filename)  # Remove the screenshot file after sending
        elif request == "exit":
            print("Exiting...")
            break

    conn.close()
    s.close()
