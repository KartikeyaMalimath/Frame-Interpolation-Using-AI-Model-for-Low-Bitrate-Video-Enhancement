import os
import re
import requests

import tensorflow as tf
import tensorflow_hub as hub
import mediapy as media
import numpy as np

from msc_project.interpolator import Interpolator
from typing import Generator, Iterable, List

Interpolator = Interpolator()
model = hub.load("https://tfhub.dev/google/film/1")

_UINT8_MAX_F = float(np.iinfo(np.uint8).max)

def load_image(img_path: str):

    if(img_path.startswith("http")):
        response = requests.get(img_path)
        image_data = response.content
    else:
        image_data = tf.io.read_file(img_path)

    image = tf.io.decode_image(image_data, channels=3)
    image_numpy = tf.cast(image, dtype=tf.float32).numpy()
    return image_numpy/_UINT8_MAX_F

def _recursive_generator(frame1: np.ndarray, frame2: np.ndarray, num: int, interpolator: Interpolator) -> Generator[np.ndarray, None, None]:
    if num == 0:
        yield frame1
    else:
        time = np.full(shape=(1,), fill_value=0.5, dtype=np.float32)
        intermediate_frame = interpolator(np.expand_dims(frame1, axis=0),
                                          np.expand_dims(frame2, axis=0), time)[0]
        yield from _recursive_generator(frame1, intermediate_frame, num-1, interpolator)
        yield from _recursive_generator(intermediate_frame, frame2, num-1, interpolator)

def recursive_interpolate(frames: List[np.ndarray], num: int, interpolator: Interpolator) -> Iterable[np.ndarray]:
    n = len(frames)
    for i in range(1, n):
        yield from _recursive_generator(frames[i-1], frames[i], num, interpolator)
    yield frames[-1]

if __name__ == "__main__":
    num_of_interpolate_frames = 4
    input_data_path = "./test/"
    file_names = os.listdir(input_data_path)

    sorted_file_names = sorted(file_names, key=lambda x: [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', x)])
    loaded_image_list = []
    for file in sorted_file_names:
        load_img = load_image(input_data_path+file)
        loaded_image_list.append(load_img)
    output_frames = list(recursive_interpolate(loaded_image_list, num_of_interpolate_frames, Interpolator))
    for i in range(len(output_frames)):
        media.write_image(path=f"./test_process/frame{i}.png", image=output_frames[i])
    # media.write_video("./output/output_video2.mp4", images=output_frames, fps=30)







