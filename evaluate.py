# Import OpenCV
import cv2

# Import Matplotlib
import matplotlib.pyplot as plt

# Import NumPy
import numpy as np

# Import scikit-image
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim

# Define the paths of the normal video and the interpolated video
normal_video_path = "input/reduced_fps_video_8_fps.mp4"
interpolated_video_path = "output/output_31.0_fps.mp4"

# Create video capture objects for both videos
normal_video = cv2.VideoCapture(normal_video_path)
interpolated_video = cv2.VideoCapture(interpolated_video_path)

# Check if both videos are opened successfully
if not normal_video.isOpened():
    print("Error opening normal video")
    exit()
if not interpolated_video.isOpened():
    print("Error opening interpolated video")
    exit()

# Initialize some lists for storing the metrics
psnr_list = [] # List of PSNR values for each frame pair
ssim_list = [] # List of SSIM values for each frame pair
frame_list = [] # List of frame numbers

# Loop through both videos frame by frame
while True:
    # Read a frame from each video
    normal_ret, normal_frame = normal_video.read()
    interpolated_ret, interpolated_frame = interpolated_video.read()

    # Check if both frames are read successfully
    if not normal_ret or not interpolated_ret:
        break

    # Convert both frames to grayscale
    normal_frame_gray = cv2.cvtColor(normal_frame, cv2.COLOR_BGR2GRAY)
    interpolated_frame_gray = cv2.cvtColor(interpolated_frame, cv2.COLOR_BGR2GRAY)

    # Calculate PSNR between the frames using scikit-image
    psnr_value = psnr(normal_frame_gray, interpolated_frame_gray)

    # Calculate SSIM between the frames using scikit-image
    ssim_value = ssim(normal_frame_gray, interpolated_frame_gray)

    # Append the metrics values and frame number to the lists
    psnr_list.append(psnr_value)
    ssim_list.append(ssim_value)
    frame_list.append(len(frame_list) + 1)

# Release the video capture objects
normal_video.release()
interpolated_video.release()

# Plot PSNR values as a line chart using Matplotlib
plt.plot(frame_list, psnr_list)
plt.xlabel("Frame Number")
plt.ylabel("PSNR")
plt.title("PSNR vs Frame Number")
plt.show()

# Plot SSIM values as a line chart using Matplotlib
plt.plot(frame_list, ssim_list)
plt.xlabel("Frame Number")
plt.ylabel("SSIM")
plt.title("SSIM vs Frame Number")
plt.show()




