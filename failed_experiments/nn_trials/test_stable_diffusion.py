import keras_cv
import torch
from PIL import Image
import torchvision.transforms as transforms
import numpy as np
import tensorflow as tf

# Create a MirroredStrategy
strategy = tf.distribute.MirroredStrategy()

# Move everything under the strategy scope
with strategy.scope():
  # Define the custom image_encoder layer as a subclass of tf.keras.layers.Layer
  class CustomImageEncoder(tf.keras.layers.Layer):
    def __init__(self):
      super(CustomImageEncoder, self).__init__()
      self.conv1 = tf.keras.layers.Conv2D(64, (4, 4), strides=2, padding="same", activation="relu")
      self.conv2 = tf.keras.layers.Conv2D(128, (4, 4), strides=2, padding="same", activation="relu")
      self.conv3 = tf.keras.layers.Conv2D(256, (4, 4), strides=2, padding="same", activation="relu")

    def call(self, inputs):
      x = self.conv1(inputs)
      x = self.conv2(x)
      x = self.conv3(x)
      return x

  # Define the custom decoder layer as a subclass of tf.keras.layers.Layer
  class CustomDecoder(tf.keras.layers.Layer):
    def __init__(self):
      super(CustomDecoder, self).__init__()
      self.conv1 = tf.keras.layers.Conv2DTranspose(128, (4, 4), strides=2, padding="same", activation="relu")
      self.conv2 = tf.keras.layers.Conv2DTranspose(64, (4, 4), strides=2, padding="same", activation="relu")
      self.conv3 = tf.keras.layers.Conv2DTranspose(32, (4, 4), strides=2, padding="same", activation="relu")
      self.conv4 = tf.keras.layers.Conv2DTranspose(16, (4, 4), strides=2, padding="same", activation="relu")
      self.conv5 = tf.keras.layers.Conv2DTranspose(3, (4, 4), strides=2, padding="same", activation="sigmoid")

    def call(self, inputs):
      x = self.conv1(inputs)
      x = self.conv2(x)
      x = self.conv3(x)
      x = self.conv4(x)
      x = self.conv5(x)
      return x

  # Create a subclassed model with the image_encoder layer as an attribute
  class CustomModel(tf.keras.Model):
    def __init__(self):
      super(CustomModel, self).__init__()
      # Define the image_encoder layer as an attribute
      self.image_encoder = keras_cv.models.StableDiffusion(img_height=512, img_width=512).image_encoder
      # Define the other layers as usual
      self.decoder = keras_cv.models.StableDiffusion(img_height=512, img_width=512).decoder

    def call(self, inputs):
      # Define the forward pass of the model
      x = self.image_encoder(inputs)
      x = self.decoder(x)
      return x

  # Create an instance of the subclassed model
  model = CustomModel()
  # Replace the image_encoder layer with the custom one
  model.image_encoder = CustomImageEncoder()
  # Replace the decoder layer with the custom one
  model.decoder = CustomDecoder()

def generate_interpolated_frame(frame1, frame2, steps=100):
  """Generates an interpolated frame between two input frames using keras_cv.

  Args:
    frame1: The first input frame.
    frame2: The second input frame.
    steps: The number of steps to run the keras_cv diffusion process.

  Returns:
    The interpolated frame.
  """

  # Convert the torch tensors to numpy arrays.
  frame1 = frame1.numpy()
  frame2 = frame2.numpy()

  # Resize the numpy arrays to (800, 800).
  frame1 = tf.image.resize(frame1, (800, 800))
  frame2 = tf.image.resize(frame2, (800, 800))

  # Check if the images are grayscale and convert them to RGB if they are.
  if tf.shape(frame1)[-1] == 1:
    frame1 = tf.image.grayscale_to_rgb(frame1)
  if tf.shape(frame2)[-1] == 1:
    frame2 = tf.image.grayscale_to_rgb(frame2)

  # Create a latent representation of the first frame.
  latent1 = model.image_encoder(frame1)

  # Create a latent representation of the second frame.
  latent2 = model.image_encoder(frame2)

  # Generate an interpolated latent representation.
  latent_interp = (latent1 + latent2) / 2

  # Reshape the input tensor to match the expected shape of the decoder layer
  latent_interp = tf.reshape(latent_interp, (1, 64, 64, 16))

  # Generate the interpolated frame.
  frame_interp = model.decoder(latent_interp)

  # Convert the numpy array to a torch tensor.
  frame_interp = torch.from_numpy(frame_interp)

  return frame_interp

if __name__ == "__main__":
  # Define the transformation to convert PIL images to torch tensors and add a dimension.
  transform = transforms.Compose([transforms.ToTensor(), lambda x: x.unsqueeze(0)])

  # Load the input frames and apply the transformation.
  frame1 = transform(Image.open("./data/frame_0.jpg"))
  frame2 = transform(Image.open("./data/frame_1.jpg"))

  # Generate the interpolated frame.
  frame_interp = generate_interpolated_frame(frame1, frame2)

  # Save the interpolated frame.
  torch.save(frame_interp, "frame_interp.jpg")
