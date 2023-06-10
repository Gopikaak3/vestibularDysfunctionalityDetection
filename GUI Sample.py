import cv2
import tkinter as tk
from PIL import Image, ImageTk
from threading import Thread

class VideoApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Video App")

        # Initialize OpenCV VideoCapture object
        self.video = cv2.VideoCapture(0)
        self.is_running = False
        self.is_recording = False

        # Create a canvas to display the video feed
        self.canvas = tk.Canvas(window, width=800, height=600)
        self.canvas.pack()

        # Create buttons
        self.start_button = tk.Button(window, text="Start", command=self.start)
        self.start_button.pack(side=tk.LEFT)

        self.stop_button = tk.Button(window, text="Stop", command=self.stop)
        self.stop_button.pack(side=tk.LEFT)

        self.record_button = tk.Button(window, text="Record", command=self.record)
        self.record_button.pack(side=tk.LEFT)

        self.update()

    def start(self):
        if not self.is_running:
            self.is_running = True
            # Create a new thread to continuously read video frames
            self.video_thread = Thread(target=self.video_loop)
            self.video_thread.start()

    def stop(self):
        if self.is_running:
            self.is_running = False
            self.video_thread.join()

    def record(self):
        if not self.is_recording:
            self.is_recording = True
            # Create a new thread to continuously record frames
            self.record_thread = Thread(target=self.record_loop)
            self.record_thread.start()
        else:
            self.is_recording = False

    def video_loop(self):
        while self.is_running:
            ret, frame = self.video.read()
            if ret:
                # Mirror the frame horizontally
                frame = cv2.flip(frame, 1)
                # Convert the frame to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Resize the frame to fit the canvas
                frame = cv2.resize(frame, (800, 600))
                # Create an ImageTk object from the frame
                image = Image.fromarray(frame)
                image_tk = ImageTk.PhotoImage(image)
                # Update the canvas with the new image
                self.canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)
                self.canvas.image = image_tk

    def record_loop(self):
        out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480))
        while self.is_recording:
            ret, frame = self.video.read()
            if ret:
                # Write the frame to the output video file
                out.write(frame)
        out.release()

    def update(self):
        # Update the GUI every 10 milliseconds
        self.window.after(10, self.update)

if __name__ == '__main__':
    root = tk.Tk()
    app = VideoApp(root)
    root.mainloop()
