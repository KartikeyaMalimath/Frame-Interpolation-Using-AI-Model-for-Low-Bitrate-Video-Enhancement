
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import cv2 # Import OpenCV
from tensorflow.keras import Model
from tensorflow.keras.layers import Input, Dense, Flatten, Reshape

# Define the input shape
input_shape = (512,1024, 3)
# Define the encoder network
encoder = keras.Sequential(
    [
        layers.Input(shape=(512, 1024, 3)), # Swap the width and height dimensions
        layers.Conv2D(64, 3, strides=2, padding="same", activation="relu"),
        layers.Conv2D(128, 3, strides=2, padding="same", activation="relu"),
        layers.Conv2D(256, 3, strides=2, padding="same", activation="relu"),
        layers.Conv2D(512, 3, strides=2, padding="same", activation="relu"),
    ],
    name="encoder",
)
# Define the decoder network
decoder = keras.Sequential(
    [
        layers.Input(shape=(32, 64, 512)), # Change the input shape to match the encoder output shape
        layers.Conv2DTranspose(256, 3, strides=2, padding="same", activation="relu"),
        layers.Conv2DTranspose(128, 3, strides=2, padding="same", activation="relu"),
        layers.Conv2DTranspose(64, 3, strides=2, padding="same", activation="relu"),
        layers.Conv2DTranspose(3, 3, strides=2, padding="same", activation="sigmoid"),
    ],
    name="decoder",
)
# Define the interpolation network
interpolation = keras.Sequential(
    [
        layers.Input(shape=(32, 64, 1024)),
        layers.Dense(512),
        layers.Dense(256),
        layers.Dense(128),
        layers.Dense(512),
    ],
    name="interpolation",
)

# Define the model that takes two frames as input and outputs an interpolated frame
class InterpolationModel(Model):
    def __init__(self):
        super(InterpolationModel, self).__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.interpolation = interpolation

    def call(self, inputs):
        frame1 = inputs[:, 0]
        frame2 = inputs[:, -1]
        encoded1 = self.encoder(frame1)
        encoded2 = self.encoder(frame2)
        concatenated = layers.Concatenate(axis=-1)([encoded1, encoded2])
        interpolated = self.interpolation(concatenated)
        decoded = self.decoder(interpolated)
        return decoded

# Create a new model from the InterpolationModel class
model = InterpolationModel()
inputs = keras.Input(shape=(None,) + input_shape)
# Pass the inputs tensor directly to the model
new_model = Model(inputs, model(inputs)) # Use the Model(inputs, outputs) syntax instead of the model(inputs) syntax
# Print the model summary
new_model.summary()

# Read two custom input images from disk
img1 = cv2.imread("../../data/frame_1.png")
img2 = cv2.imread("../../data/frame_2.png")
# Resize the input images to 512 by 1024 pixels
img1 = tf.image.resize(img1, (512, 1024))
img2 = tf.image.resize(img2, (512, 1024))

# Reshape the input tensors to match the expected shape of the input to the encoder layer
img1 = tf.expand_dims(img1, axis=0) # Add a batch dimension of 1 to img1
img2 = tf.expand_dims(img2, axis=0) # Add a batch dimension of 1 to img2
# Stack the two images along the time dimension
img = tf.stack([img1, img2], axis=1) # Create a tensor of shape (1, 2, 512, 1024, 3)
# Predict the interpolated image using the model
img = model.predict(img)[0] # Pass the tensor directly to the model
# Reshape the output tensor to match the input shape
img = tf.reshape(img, (-1, 512, 1024, 3))
# Convert the image to uint8 format using tf.cast
img = tf.cast(img * 255, dtype=tf.uint8)
# Squeeze the image tensor to remove the singleton dimension
img = tf.squeeze(img)
# Encode the image as a JPEG string using tf.io.encode_jpeg
img = tf.io.encode_png(img)
# Write the image file using tf.io.write_file
tf.io.write_file("../custom_frame_interpolated.png", img)
