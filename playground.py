# # Using ffprobe
# import subprocess
# import json
#
# video_file = "reduce_fps_processing/reduced_fps_video_8_fps.mp4"
#
# # Invoke ffprobe with subprocess.check_output
# output = subprocess.check_output(["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", video_file])
#
# # Parse the output as JSON
# data = json.loads(output)
#
# # Print the format and codec information
# print(data["format"]["format_name"])
# print(data["streams"][0]["codec_name"])
import time

import psutil

# Python program to find factors of a number using a loop and a set

# Python program to find factors of a number using a loop and a set

# Take input from user
# num = int(input("Enter a number: "))
#
# # Initialize an empty set to store the factors
# factors = set()
#
# # Loop from 1 to num
# for i in range(1, num + 1):
#     # Check if i is a factor of num
#     if num % i == 0:
#         # Add i to the set of factors
#         factors.add(i)
#
# # Print the result
# print("The factors of", num, "are:", factors)
#
# # Initialize a variable to store the least fps
# least_fps = None
#
# # Loop from 8 to 12
# for fps in range(7, 15):
#     # Check if fps is a factor of num
#     if fps in factors:
#         # Assign fps to least_fps
#         least_fps = fps
#         # Break out of the loop
#         break
#
# # Check if least_fps is found
# if least_fps is not None:
#     # Print the result
#     print("The least fps between 8 and 12 that you can choose for", num, "is:", least_fps)
# else:
#     # Print a message
#     print("There is no fps between 8 and 12 that you can choose for", num)

while True:
    # Get the CPU and RAM usage
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    print(cpu_usage)
    print(ram_usage)
    time.sleep(5)
