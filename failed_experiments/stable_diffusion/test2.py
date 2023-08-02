import tensorflow as tf
import tensorflow_hub as hub

# Load the film interpolation model from TensorFlow Hub.
model = hub.load("https://tfhub.dev/google/film/interpolate/1")

# Read the two input images.
frame1 = tf.image.decode_image(tf.read_file("../data/frame_0.png"))
frame2 = tf.image.decode_image(tf.read_file("../data/frame_1.png"))

# Interpolate the two images.
interpolated_image = model(frame1, frame2)

# Save the interpolated image.
tf.image.write_file("interpolated_image.jpg", interpolated_image)
