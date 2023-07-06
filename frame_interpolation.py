import os
import cv2
import numpy as np
import requests

# Constants
input_fps = 10
target_fps = 30
api_endpoint = "https://api.dalle.com/interpolate"

# Input and output video paths
input_frames_directory = "./data"
output_video_path = "./output/outputvideo.mp4"

# Get the list of frames in the input frames directory
frames = sorted(os.listdir(input_frames_directory))

# Initialize list to store interpolated frames
interpolated_frames = []

# Iterate over the frames (excluding the last frame)
for i in range(len(frames) - 1):
    # Load consecutive frames
    frame1_path = os.path.join(input_frames_directory, frames[i])
    frame2_path = os.path.join(input_frames_directory, frames[i + 1])
    frame1 = cv2.imread(frame1_path)
    frame2 = cv2.imread(frame2_path)

    # Preprocess frames as needed
    # (e.g., resize, convert color channels, etc.)

    # Prepare frames for input to DALL-E API
    # (e.g., convert to base64, create request payload, etc.)
    frame1_base64 = cv2.imencode(".jpg", frame1)[1].tostring()
    frame2_base64 = cv2.imencode(".jpg", frame2)[1].tostring()
    payload = {
        "frame1": frame1_base64,
        "frame2": frame2_base64,
        "alpha": 1 / (target_fps / input_fps)
    }

    # Send request to DALL-E API for interpolation
    response = requests.post(api_endpoint, json=payload)
    interpolated_frame = np.array(response.json()["interpolated_frame"])

    # Postprocess interpolated frame as needed
    # (e.g., convert color spaces, adjust pixel values, etc.)

    # Append interpolated frame to list
    interpolated_frames.append(interpolated_frame)

# Convert interpolated frames to video
output_width, output_height = interpolated_frames[0].shape[1], interpolated_frames[0].shape[0]
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
output_video = cv2.VideoWriter(output_video_path, fourcc, target_fps, (output_width, output_height))

for frame in interpolated_frames:
    output_video.write(frame)

# Release the video writer
output_video.release()

print(f"Interpolated video saved to: {output_video_path}")
