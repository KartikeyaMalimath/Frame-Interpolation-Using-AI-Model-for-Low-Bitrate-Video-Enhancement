import cv2
import moviepy.editor
import subprocess
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class ReduceFPS():
    """A class that reduces the frame rate of a video file."""

    def __init__(self, **kwargs):
        self.input_file = kwargs.get("input_file")
        self.fps = kwargs.get("fps")
        self.processing_video = os.path.join("reduce_fps_processing", "processing_video_only.mp4")
        self.processing_audio = os.path.join("reduce_fps_processing", "processing_audio_only.mp3")

    def fps_calculation(self, fps):
        # Initialize an empty set to store the factors
        factors = set()
        # Loop from 1 to num
        for i in range(1, fps + 1):
            # Check if i is a factor of num
            if fps % i == 0:
                # Add i to the set of factors
                factors.add(i)
        # Print the result
        print("The factors of", fps, "are:", factors)
        # Initialize a variable to store the selected fps
        select_fps = None
        if self.fps == 0:
            #Loop from 7 to 11
            select_fps = self.select_loop(factors=factors, start=7, end=11, step=1)
        elif self.fps == 1:
            # Loop from 10 to 15
            select_fps = self.select_loop(factors=factors, start=15, end=10, step=-1)
        if select_fps:
            return select_fps
        else:
            return 10

    def select_loop(self, factors, start, end, step):
        for fps in range(start, end, step):
            # Check if fps is a factor of num
            if fps in factors:
                # Assign fps to least_fps
                select_fps = fps
                # Break out of the loop
                return select_fps

    def fps_reduction(self):
        """A method that reduces the frame rate of the input video file and returns True if successful, False otherwise."""
        # Check if the input is valid
        try:
            # Create a video capture object to read the input video
            cap = cv2.VideoCapture(self.input_file)

            # Get the original frame rate, width, height, and number of frames
            original_fps = cap.get(cv2.CAP_PROP_FPS)

            #calculate the least FPS or Intermediate FPS that the video can be converted to
            fps = self.fps_calculation(int(original_fps))
            output_file = os.path.join("reduce_fps_processing", f"reduced_fps_video_{fps}_fps.mp4")

            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            # Create a video writer object to write the output video
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            out = cv2.VideoWriter(self.processing_video, fourcc, fps, (width, height))

            # Initialize a counter variable for counting frames
            counter = 0

            # Calculate the skip factor based on the reduced frame rate
            skip_factor = int(original_fps / fps)

            # Loop over the frames of the input video
            while cap.isOpened():
                # Read a frame from the input video
                ret, frame = cap.read()

                # Check if there is a valid frame
                if ret:
                    # Increment the counter
                    counter += 1

                    # Check if this frame should be written or skipped
                    # For example, if we want to reduce the frame rate from 24 to 8,
                    # we can write every third frame by checking if the counter is divisible by 3
                    if counter % skip_factor == 0:
                        # Write this frame to the output video
                        out.write(frame)
                else:
                    # Break out of the loop if there is no more frames
                    break

            # Release the video capture and writer objects
            cap.release()
            out.release()

            # Create a video clip object from the input file name
            video_clip = moviepy.editor.VideoFileClip(self.input_file)

            # Get the audio clip object from the video clip object
            audio_clip = video_clip.audio

            # Write the audio clip object to an MP3 file
            audio_clip.write_audiofile(self.processing_audio)

            # Merge the output video file and the audio file into a final video file with audio
            command = f"ffmpeg -i {self.processing_video} -i {self.processing_audio} -c:v libx264 -c:a copy {output_file} "
            subprocess.call(command, shell=True)

            logging.info("Video reduced successfully!")

            return output_file

        except Exception as e:
            logging.error(f"An error occurred while reducing the video: {e}")

            return False


if __name__ == "__main__":
    input_file = "reduce_fps_processing/dana-dancing-3d-animation-maya-y2bs.com.mp4"
    # user input to choose the reduced frame rate
    print("Please choose the reduced frame rate: 8 or 16")
    reduced_fps = int(input())
    reduce_fps_handler = ReduceFPS(input_file=input_file, fps=reduced_fps)
    return_handler = reduce_fps_handler.fps_reduction()
    if return_handler:
        print(f"Final video saved")
    else:
        print("error reducing FPS")
