import os
import glob
import numpy as np
import tensorflow as tf
import cv2
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import MeanSquaredError
from custom_nn2 import InterpolationModel

# Define some hyperparameters
batch_size = 8 # You can change this according to your memory capacity
epochs = 10 # You can change this according to your desired training time
learning_rate = 0.001 # You can change this according to your optimization strategy

# Define a function to load and preprocess the images from a given folder
def load_images(path):
    # Get all the image paths from the folder using glob
    image_paths = glob.glob(os.path.join(path, "*.png"))
    # Sort the image paths by their names
    image_paths = sorted(image_paths)
    # Initialize an empty list to store the images
    images = []
    # Loop through each image path
    for image_path in image_paths:
        # Read the image using cv2.imread
        image = cv2.imread(image_path)
        # Resize the image to 512 by 1024 pixels using tf.image.resize
        image = tf.image.resize(image, (512, 1024))
        # Normalize the image to [0, 1] range using tf.divide
        image = tf.divide(image, 255.0)
        # Append the image to the images list
        images.append(image)
    # Create a dataset from the images list using tf.data.Dataset.from_tensor_slices
    dataset = tf.data.Dataset.from_tensor_slices(images).batch(batch_size)
    # Return the dataset instead of the images tensor
    return dataset

# Load the images from the HD_data folder using the load_images function
input_dataset = load_images("../../HD_data")
# Load the images from the data folder using the load_images function
target_dataset = load_images("../../data")
# Zip the input and target datasets with a one-step offset to create pairs of two input images and one target image
dataset = tf.data.Dataset.zip((input_dataset.skip(1), input_dataset, target_dataset))
# Batch the dataset with the desired batch size
dataset = dataset.batch(batch_size)
# Train the model using model.fit with dataset as input and output respectively
model = InterpolationModel()
def custom_loss(target, output):
    return tf.keras.losses.MeanSquaredError()(tf.squeeze(output, axis=0), target)

model.compile(optimizer="adam", loss=custom_loss)

model.fit(dataset, epochs=epochs)
# Save the model as a HDF5 file using model.save
model.save("interpolation_model.h5")
