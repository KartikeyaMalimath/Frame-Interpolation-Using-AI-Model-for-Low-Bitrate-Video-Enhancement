import moviepy.editor as mp
import glob
import os

# Define the input audio file name
audio_file = "input/input_8fps_audio.mp3"

# Get the list of frame files in the /data folder
frame_files = sorted(glob.glob("D:\\University_of_Leeds\\MSc Project\\msc_project\\data\\*.png"), key=os.path.getmtime)

# Get the number of frames in the /data folder
frame_count = len(frame_files)

# Check if the audio file exists
if os.path.exists(audio_file):
    # Create an audio clip object from the audio file
    audio = mp.AudioFileClip(audio_file)

    # Get the duration of the audio clip in seconds
    duration = audio.duration

else:
    # Ask the user to enter the duration of the video in seconds
    duration = float(input("Please enter the duration of the video in seconds: "))

# Calculate the frame rate based on the number of frames and the duration
fps = frame_count / duration
fps = round(fps, 1)
# Define the output file name with the frame rate
output_file = f"output/output_{fps}_fps.mp4"

# Create a video clip object from the list of frame files
clip = mp.ImageSequenceClip(frame_files, fps=fps)

# Set the audio of the video clip to the audio clip if it exists
if os.path.exists(audio_file):
    clip = clip.set_audio(audio)

# Write the video clip object to the output video file
clip.write_videofile(output_file)
