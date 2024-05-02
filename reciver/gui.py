import tkinter as tk
from tkinter import ttk
from receiver import ScreenshotReceiver
from PIL import Image, ImageTk

class ReceiverGUI:
    def __init__(self):
        self.receiver = ScreenshotReceiver()
        self.root = tk.Tk()
        self.root.title("Screenshot Receiver")

        # Configure style for ttk widgets
        self.style = ttk.Style()
        self.style.configure('TButton', padding=6, relief="flat", background="#4CAF50", foreground="white")
        self.style.map('TButton', background=[('active', '#45a049')])

        # Main frame
        self.main_frame = ttk.Frame(self.root, padding=(20, 10))
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Buttons
        self.btn_request = ttk.Button(self.main_frame, text="Request Screenshot", command=self.request_screenshot)
        self.btn_request.pack(pady=(0, 10))

        self.btn_exit = ttk.Button(self.main_frame, text="Exit", command=self.exit_app)
        self.btn_exit.pack()

        self.btn_zoom_in = ttk.Button(self.main_frame, text="Zoom In", command=lambda: self.scale_image(1.1))
        self.btn_zoom_in.pack(side=tk.LEFT, padx=10)

        self.btn_zoom_out = ttk.Button(self.main_frame, text="Zoom Out", command=lambda: self.scale_image(0.9))
        self.btn_zoom_out.pack(side=tk.LEFT)

        # Status label
        self.lbl_status = ttk.Label(self.main_frame, text="", foreground="red")
        self.lbl_status.pack(pady=(10, 0))

        # Image label
        self.img_label = ttk.Label(self.main_frame)
        self.img_label.pack(pady=(10, 0))

        # Set window minimum size and center it
        self.root.minsize(400, 300)
        self.center_window()

        # Image properties
        self.image = None
        self.current_scale = 1.0

        # Bind close event to handle receiver closing
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)

    def request_screenshot(self):
        try:
            self.receiver.request_screenshot()
            screenshot_data = self.receiver.receive_screenshot()
            filename = self.receiver.save_screenshot(screenshot_data)
            self.lbl_status.config(text=f"Screenshot received and saved as '{filename}'", foreground="green")
            self.load_image(filename)
        except Exception as e:
            self.lbl_status.config(text=f"Error: {e}", foreground="red")

    def load_image(self, filename):
        img = Image.open(filename)
        self.image = ImageTk.PhotoImage(img)
        self.img_label.config(image=self.image)

    def scale_image(self, factor):
        self.current_scale *= factor
        width = int(self.image.width() * self.current_scale)
        height = int(self.image.height() * self.current_scale)
        img = self.image.resize((width, height), Image.LANCZOS)
        self.img_label.config(image=img)
        self.img_label.image = img

    def exit_app(self):
        try:
            self.receiver.close()
        except Exception as e:
            print(f"Error while closing connection: {e}")
        self.root.destroy()

    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = self.root.winfo_reqwidth()
        window_height = self.root.winfo_reqheight()
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    receiver_gui = ReceiverGUI()
    receiver_gui.run()
