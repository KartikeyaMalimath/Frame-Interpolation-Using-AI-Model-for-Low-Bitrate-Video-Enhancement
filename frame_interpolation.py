import keras_cv
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# Load stable diffusion model
model = keras_cv.models.StableDiffusion(jit_compile=True)

frame1_path = "./data/frame_0.jpg"
frame2_path = "./data/frame_1.jpg"

# Read and decode the images from the paths
frame1 = tf.image.decode_image(tf.io.read_file(frame1_path))
frame2 = tf.image.decode_image(tf.io.read_file(frame2_path))

# Resize the images to a smaller size
frame1 = tf.image.resize(frame1, [224, 224])
frame2 = tf.image.resize(frame2, [224, 224])

# Add a batch dimension to the frames
frame1 = tf.expand_dims(frame1, axis=0)
frame2 = tf.expand_dims(frame2, axis=0)

# Encode the frames into latent vectors
latent1 = model.image_encoder(frame1)
latent2 = model.image_encoder(frame2)

# Interpolate the latent vectors at a given ratio
ratio = 0.5
latent_interp = model.generate_image(latent1, latent2)

# Decode the interpolated latent vector into an image
image_interp = model.decoder(latent_interp)

# Display the image
plt.imshow(image_interp)
plt.show()
