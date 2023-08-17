# Import the libraries
import cv2
from moviepy.editor import *


class SplitFrame:
    def __init__(self, **kwargs):
        # Define the input and output paths
        self.video_path = kwargs.get("input_video_path") # The path of the input video file
        self.data_path = "data/"  # The path of the folder where the frames will be stored
        self.audio_path = "audio_temp/"  # The path of the folder where the audio will be stored
        self.audio_file_name = "temp_audio.mp3"

    def split_frame(self):
        # Read the video file using OpenCV
        video = cv2.VideoCapture(self.video_path)
        # Get the frame rate and number of frames of the video
        fps = video.get(cv2.CAP_PROP_FPS)
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        # Loop through the frames of the video
        for i in range(frame_count):
            # Read the next frame
            success, frame = video.read()
            # If successful, save the frame as an image file in the data folder
            if success:
                cv2.imwrite(self.data_path + "frame_" + str(i) + ".jpg", frame)
            # Otherwise, break the loop
            else:
                break
        # Release the video object
        video.release()

    def split_audio(self):
        import subprocess

        output = subprocess.run(
            ["ffprobe", "-i", self.video_path, "-show_streams", "-select_streams", "a", "-loglevel", "error"],
            capture_output=True, text=True).stdout
        if output:
            # Load the video file as an audio clip
            audio = AudioFileClip(self.video_path)
            audio.write_audiofile(self.audio_path + self.audio_file_name)
        else:
            print("The video has no audio.")



if __name__ == "__main__":
    split_frame_handler = SplitFrame(input_video_path="input/output_2.8_fps.mp4")
    split_frame_handler.split_frame()  # split input video to frame images
    split_frame_handler.split_audio()  # split and store audio from the input video