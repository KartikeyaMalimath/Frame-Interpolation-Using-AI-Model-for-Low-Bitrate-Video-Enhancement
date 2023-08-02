import os
import re

import cv2

def frames_to_video(frames_directory, output_video_path, fps):
    # Get the list of frames in the directory
    frames = sorted(os.listdir(frames_directory), key=lambda x: [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', x)])
    print(frames)

    # Read the first frame to get frame size
    first_frame_path = os.path.join(frames_directory, frames[0])
    first_frame = cv2.imread(first_frame_path)
    height, width, _ = first_frame.shape

    # Set a fixed frame size for the output video
    frame_size = (width, height)

    # Initialize the video writer
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, frame_size)

    # Iterate over the frames and write them to the video
    for frame_name in frames:
        frame_path = os.path.join(frames_directory, frame_name)
        frame = cv2.imread(frame_path)

        # # Resize the frame if it has a different size
        # if frame.shape[:2] != frame_size:
        #     frame = cv2.resize(frame, frame_size)

        # Write the frame to the video
        video_writer.write(frame)

    # Release the video writer
    video_writer.release()

    print(f"Video saved to: {output_video_path}")

if __name__ == "__main__":
    frames_directory = "D:\\University_of_Leeds\\MSc Project\\msc_project\\test_process\\"
    output_video_path = "D:\\University_of_Leeds\\MSc Project\\msc_project\\output\\outputvideo3.mp4"
    fps = 10
    frames_to_video(frames_directory, output_video_path, fps)
