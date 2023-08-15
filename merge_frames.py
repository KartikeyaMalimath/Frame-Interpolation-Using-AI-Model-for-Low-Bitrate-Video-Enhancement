import re
import moviepy.editor as mp
import glob
import os

class MergeFrames:

    def __init__(self, **kwargs):

        # Define the input audio file name
        self.audio_file = "audio_temp/temp_audio.mp3"
        self.frames_file = "D:\\University_of_Leeds\\MSc Project\\msc_project\\processing\\"

        self.file_names = os.listdir(self.frames_file)
        # Get the list of frame files in the /data folder
        self.frame_files = sorted(self.file_names, key=lambda x: [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', x)])

        # Get the number of frames in the /data folder
        self.frame_count = len(self.frame_files)

        # Check if the audio file exists
        if os.path.exists(self.audio_file):
            # Create an audio clip object from the audio file
            self.audio = mp.AudioFileClip(self.audio_file)

            # Get the duration of the audio clip in seconds
            self.duration = self.audio.duration
        elif kwargs.get("duration"):
            self.duration = kwargs.get("duration")
        else:
            # Ask the user to enter the duration of the video in seconds
            self.duration = float(input("Please enter the duration of the video in seconds: "))

    def merge_frames(self):
        # Calculate the frame rate based on the number of frames and the duration
        fps = self.frame_count / self.duration
        fps = round(fps, 1)
        # Define the output file name with the frame rate
        output_file = f"output/output_{fps}_fps.mp4"

        full_image_paths = [os.path.join(self.frames_file, file) for file in self.frame_files]
        # Create a video clip object from the list of frame files
        clip = mp.ImageSequenceClip(full_image_paths, fps=fps)

        # Set the audio of the video clip to the audio clip if it exists
        if os.path.exists(self.audio_file):
            clip = clip.set_audio(self.audio)

        # Write the video clip object to the output video file
        clip.write_videofile(output_file)
        return output_file

if __name__ == "__main__":
    merge_frame_handler = MergeFrames()
    merge_frame_handler.merge_frames()