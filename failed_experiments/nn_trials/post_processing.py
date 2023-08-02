# Import some libraries for image processing
import numpy as np
import skimage
import PIL
import tensorflow as tf
from torch import hub

# Load the interpolated image from disk
img = tf.io.read_file("custom_frame_interpolated.jpg")
img = tf.io.decode_jpeg(img)

# Convert the image to float32 and normalize it to [0..1] range
img = tf.image.convert_image_dtype(img, tf.float32)

# Apply some image denoising method, such as bilateral filter
img = tf.image.adjust_saturation(img, saturation_factor=0.05) # use tf.image to adjust the saturation of the tensor
img = tf.image.adjust_contrast(img, contrast_factor=15) # use tf.image to adjust the contrast of the tensor
img = img.numpy() # convert the tensor to a numpy array
img = skimage.restoration.denoise_bilateral(img, sigma_color=0.05, sigma_spatial=15, channel_axis=-1) # use skimage to apply the bilateral filter on the array

# Apply some image sharpening method, such as unsharp masking
img = skimage.filters.unsharp_mask(img, radius=1, amount=1.5, channel_axis=-1)

# Convert the image to PIL format and save it
img = PIL.Image.fromarray((img * 255).astype(np.uint8))
img.save("custom_frame_interpolated_enhanced.jpg")
