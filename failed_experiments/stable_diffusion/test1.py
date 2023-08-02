import os

import numpy as np
import cv2


def interpolate_frames(frame1, frame2, alpha):
    """
  Interpolates two frames and returns an intermediate frame.

  Args:
      frame1: The first frame.
      frame2: The second frame.
      alpha: A float value between 0 and 1 that specifies the weight of frame1 in the interpolated frame.

  Returns:
      The interpolated frame.
  """

    # Convert the frames to grayscale.
    grayscale_frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    grayscale_frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    # Scale the grayscale frames.
    grayscale_frame1 = grayscale_frame1.astype("uint8")
    grayscale_frame2 = grayscale_frame2.astype("uint8")
    cv2.imwrite("/content/sample_data/grayframe1.jpg", grayscale_frame1)

    # Interpolate the grayscale frames.
    interpolated_grayscale_frame = (alpha * grayscale_frame1 + (1 - alpha) * grayscale_frame2)

    # Convert the interpolated grayscale frame back to RGB.
    interpolated_grayscale_frame = interpolated_grayscale_frame.astype("uint8")
    interpolated_frame = cv2.cvtColor(interpolated_grayscale_frame, cv2.COLOR_GRAY2RGB)

    return interpolated_frame


if __name__ == "__main__":
  # # Define the folder path
  # folder_path = "../data/"
  #
  # # Get a list of file names in the folder
  # file_names = os.listdir(folder_path)
  #
  # # Sort the file names in alphabetical order
  # file_names = sorted(file_names)
  #
  # # Create an empty list for frame paths
  # frame_paths = []
  #
  # print(frame_paths)

  # Load the two frames.
  frame1 = cv2.imread("../../data/frame_0.png")
  frame2 = cv2.imread("../../data/frame_1.png")

  # Interpolate the frames.
  alpha = 0.5
  interpolated_frame = interpolate_frames(frame1, frame2, alpha)

  # Save the interpolated frame.
  cv2.imwrite("interpolated_frame.jpg", interpolated_frame)
