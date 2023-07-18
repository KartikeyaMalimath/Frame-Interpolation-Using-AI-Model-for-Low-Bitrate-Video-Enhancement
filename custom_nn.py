import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import cv2 # Import OpenCV
from tensorflow.keras import Model
from tensorflow.keras.layers import Input, Dense, Flatten, Reshape

# Define the input shape
input_shape = (512, 1024, 3)
# Define the encoder network
encoder = keras.Sequential(
    [
        layers.Input(shape=input_shape),
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
        layers.Input(shape=(45, 68, 1024)),
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
        concatenated = layers.Concatenate()([encoded1, encoded2])
        interpolated = self.interpolation(concatenated)
        decoded = self.decoder(interpolated)
        return decoded

# Create a Functional model that inherits from InterpolationModel
class InterpolationFunctionalModel(InterpolationModel):
    def __init__(self):
        super(InterpolationFunctionalModel, self).__init__()
        self.model = Model(
            inputs=self.encoder.inputs + self.decoder.inputs, outputs=self.decoder.outputs
        )

    def __call__(self, inputs):
        # Create a new Functional model with a Reshape layer
        reshape = layers.Reshape((-1, input_shape[2]))(self.model.output) # Create a new layer and connect it to the output of the existing model
        new_model = Model(inputs=self.model.input, outputs=reshape) # Create a new model with the same input and the new output
        return new_model

# Create a new model and add the Reshape layer
model = InterpolationFunctionalModel() # Create a new instance of the InterpolationFunctionalModel class with the updated decoder network
inputs = keras.Input(shape=(None,) + input_shape) # Define the inputs variable

# Split the input tensor into two tensors along the second dimension
img1 = inputs[:, 0] # Get the first image from the input tensor
img2 = inputs[:, -1] # Get the second image from the input tensor

new_model = model([img1, img2]) # Pass the two images as a list to the model

# Print the model summary
new_model.summary()

# Read two custom input images from disk
img1 = cv2.imread("./data/frame_0.png")
img2 = cv2.imread("./data/frame_1.png")

img1 = cv2.resize(img1, dsize=(1024, 512))
img2 = cv2.resize(img2, dsize=(1024, 512))

img1 = tf.reshape(img1, (1,) + img1.shape)
img2 = tf.reshape(img2, (1,) + img2.shape)

# Encode the input images using the encoder network
encoded1 = encoder(img1) # Get the latent vector for the first image
encoded2 = encoder(img2) # Get the latent vector for the second image

# Decode the latent vectors using the decoder network
decoded1 = decoder(encoded1) # Get the image for the first latent vector
decoded2 = decoder(encoded2) # Get the image for the second latent vector

# Predict the interpolated image using the model
img = new_model.predict([decoded1, ])[0] # Pass the images as a list to the model

# Convert the image to uint8 format and save it
img = (img * 255).astype("uint8")
cv2.imwrite("custom_frame_interpolated.jpg", img)