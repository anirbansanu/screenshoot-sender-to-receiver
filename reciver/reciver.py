import socket
import datetime

def receive_data(conn, buffer_size):
    received_data = b""
    try:
        while True:
            data_chunk = conn.recv(buffer_size)
            if not data_chunk:
                break
            received_data += data_chunk
    except socket.timeout:
        print("Socket timeout. Data reception stopped.")
    except ConnectionResetError:
        print("Connection reset by peer.")
    return received_data

def request_screenshot(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(10)  # Set a timeout of 10 seconds
        try:
            s.connect((host, port))
            s.sendall(b"send_screenshot")
            received_data = receive_data(s, 4096)  # Adjust buffer size as needed
            timestamp = datetime.datetime.now().strftime("%d-%m-%Y-%H:%M:%S")
            filename = f"{timestamp}_screenshot.png"
            with open(filename, "wb") as f:
                f.write(received_data)
            print("Screenshot received")
            s.sendall(b"Screenshot received")  # Send acknowledgment to sender
        except socket.timeout:
            print("Connection timed out. Unable to connect to the sender.")
        except ConnectionRefusedError:
            print("Connection refused. Make sure the sender is running.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    host = "127.0.0.1"  # Replace with sender's public IP or hostname
    port = 3005  # Use the same port as in the sender script

    while True:
        user_input = input("Enter 'send' to request a screenshot or 'exit' to quit: ")
        if user_input.lower() == "send":
            request_screenshot(host, port)
        elif user_input.lower() == "exit":
            print("Exiting...")
            break
        else:
            print("Invalid input. Please enter 'send' or 'exit'.")
