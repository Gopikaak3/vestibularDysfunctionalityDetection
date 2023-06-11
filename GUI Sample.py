import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
import threading

class VideoPlayer:
    def __init__(self, window, video_source=0):
        self.window = window
        self.window.title("Video Player")

        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(window, width=self.width, height=self.height)
        self.canvas.pack()

        # Buttons
        self.start_button = tk.Button(window, text="Start", width=10, command=self.start)
        self.start_button.pack(side=tk.LEFT)
        self.stop_button = tk.Button(window, text="Stop", width=10, command=self.stop)
        self.stop_button.pack(side=tk.LEFT)
        self.record_button = tk.Button(window, text="Record", width=10, command=self.record)
        self.record_button.pack(side=tk.LEFT)

        # Initialize variables
        self.playing = False
        self.recording = False
        self.delay = 15  # milliseconds
        self.update()

        self.window.mainloop()

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.read()

        if ret:
            # Convert the frame to RGB format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Mirror the frame horizontally
            frame = cv2.flip(frame, 1)

            # Convert the frame to ImageTk format
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))

            # Update the canvas with the new frame
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        if self.playing:
            self.window.after(self.delay, self.update)

    def start(self):
        if not self.playing:
            self.playing = True
            self.update()

    def stop(self):
        self.playing = False

    def record(self):
        self.recording = not self.recording

        if self.recording:
            self.record_button.config(text="Stop Recording")
            self.record_video_thread = threading.Thread(target=self.record_video)
            self.record_video_thread.start()
        else:
            self.record_button.config(text="Record")

    def record_video(self):
        # Define the codec and create a VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        output = cv2.VideoWriter("recorded_video.avi", fourcc, 20.0, (int(self.width), int(self.height)))

        while self.recording:
            ret, frame = self.vid.read()

            if ret:
                # Write the frame to the file
                output.write(frame)

        # Release the VideoWriter and close the file
        output.release()

window = tk.Tk()
app = VideoPlayer(window)
