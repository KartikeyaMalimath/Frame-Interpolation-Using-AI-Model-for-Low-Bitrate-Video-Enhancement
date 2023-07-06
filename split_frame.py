import os
import cv2

def split_video_into_frames(video_path, output_directory):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Read the video file
    video_capture = cv2.VideoCapture(video_path)

    frame_count = 0
    while True:
        # Read a frame from the video
        success, frame = video_capture.read()

        if not success:
            break

        # Generate the output file path
        output_file = os.path.join(output_directory, f"frame_{frame_count}.jpg")

        # Save the frame as an image file
        cv2.imwrite(output_file, frame)

        frame_count += 1

    # Release the video capture object
    video_capture.release()

    print(f"Split {frame_count} frames from the video.")

if __name__ == "__main__":
    video_path = "./input_10fps.mp4"
    output_directory = "D:\\University_of_Leeds\\MSc Project\\msc_project\\data\\"
    split_video_into_frames(video_path, output_directory)
