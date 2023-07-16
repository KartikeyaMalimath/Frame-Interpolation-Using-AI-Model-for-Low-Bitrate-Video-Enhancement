import cv2

def convert_video_to_fps(input_video_path, output_video_path, target_fps):
    # Open the input video
    input_video = cv2.VideoCapture(input_video_path)

    # Get the current video's properties
    fps = input_video.get(cv2.CAP_PROP_FPS)
    width = int(input_video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(input_video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create a VideoWriter object for the output video
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    output_video = cv2.VideoWriter(output_video_path, fourcc, target_fps, (width, height))

    # Calculate the frame interval to achieve the target fps
    frame_interval = int(round(fps / target_fps))

    frame_count = 0
    while True:
        # Read a frame from the input video
        ret, frame = input_video.read()

        if not ret:
            break

        if frame_count % frame_interval == 0:
            # Write the frame to the output video
            output_video.write(frame)

        frame_count += 1

    # Release the video objects
    input_video.release()
    output_video.release()

    print(f"Video converted and saved to: {output_video_path}")

if __name__ == "__main__":
    input_video_path = "./test_input_highframe.mp4"
    output_video_path = "./input_10fps.mp4"
    target_fps = 10
    convert_video_to_fps(input_video_path, output_video_path, target_fps)
