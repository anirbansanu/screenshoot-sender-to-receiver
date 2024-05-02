import tkinter as tk
from sender import ScreenshotSender

class SenderGUI:
    def __init__(self):
        self.sender = ScreenshotSender()
        self.root = tk.Tk()
        self.root.title("Screenshot Sender")
        
        self.btn_send = tk.Button(self.root, text="Send Screenshot", command=self.send_screenshot)
        self.btn_send.pack(pady=10)
        
        self.lbl_status = tk.Label(self.root, text="")
        self.lbl_status.pack()

    def send_screenshot(self):
        try:
            self.sender.establish_connection()
            self.sender.send_screenshot()
            self.lbl_status.config(text="Screenshot sent successfully")
        except Exception as e:
            self.lbl_status.config(text=f"Error: {e}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    sender_gui = SenderGUI()
    sender_gui.run()
