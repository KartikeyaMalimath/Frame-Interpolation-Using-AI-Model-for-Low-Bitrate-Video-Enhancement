import numpy as np
import tensorflow as tf
import tensorflow_hub as hub


def _pad_to_align(x, align):
    assert np.ndim(x) == 4
    assert align > 0, 'align must be positive number'

    height, width = x.shape[-3:-1]
    height_to_pad = (align - height % align) if height % align != 0 else 0
    width_to_pad = (align - width % align) if width % align != 0  else 0

    image_crop_pad = {
        'offset_height': height_to_pad // 2,
        'offset_width': width_to_pad // 2,
        'target_height': height + height_to_pad,
        'target_width': width + width_to_pad
    }

    padded_x = tf.image.pad_to_bounding_box(x, **image_crop_pad)

    image_crop = {
        'offset_height': height_to_pad // 2,
        'offset_width': width_to_pad // 2,
        'target_height': height,
        'target_width': width
    }

    return padded_x, image_crop

class Interpolator:

    def __init__(self, align: int = 64) -> None:
        self._model = hub.load("https://tfhub.dev/google/film/1")
        self._align = align

    def __call__(self, x0: np.ndarray, x1: np.ndarray, dt: np.ndarray) -> np.ndarray:
        if self._align is not None:
            x0, image_crop = _pad_to_align(x0, self._align)
            x1, _ = _pad_to_align(x1, self._align)

            inputs = {'x0': x0, 'x1': x1, 'time': dt[..., np.newaxis]}
            result = self._model(inputs, training=False)
            interpolate_image = result["image"]

            if self._align is not None:
                interpolate_image = tf.image.crop_to_bounding_box(interpolate_image, **image_crop)
            return interpolate_image.numpy()
