import os

import tensorflow as tf
import cv2
import numpy as np
import keras_cv

# Load the frames from the data folder.
frames = []
for i in range(len(os.listdir('./data'))):
    frame = cv2.imread(os.path.join('./data', f'frame_{i}.png'))
    frames.append(frame)

# Reduce the resolution of each frame to 640x480.
for i in range(len(frames)):
    frames[i] = cv2.resize(frames[i], dsize=(640, 480))

# Save the frames to a new folder.
for i in range(len(frames)):
    cv2.imwrite(os.path.join('./data_reduced', f'frame_{i:03d}.png'), frames[i])


# Load the frames from the data_reduced folder.
frames = []
for i in range(len(os.listdir('./data_reduced'))):
    frame = cv2.imread(os.path.join('./data_reduced', f'frame_{i:03d}.png'))
    frames.append(frame)

# Create a preprocessing pipeline with augmentations using keras-cv
BATCH_SIZE = 16
NUM_CLASSES = 3
augmenter = keras_cv.layers.RandAugment(value_range=(0, 255)) # use RandAugment from keras-cv

def preprocess_data(images, labels, augment=False):
    labels = tf.one_hot(labels, NUM_CLASSES)
    inputs = {"images": images, "labels": labels}
    outputs = augmenter(inputs) if augment else inputs
    return outputs['images'], outputs['labels']

train_dataset = tf.data.Dataset.from_tensor_slices((frames[:-1], frames[1:])) # create a dataset from the frames
train_dataset = train_dataset.batch(BATCH_SIZE, drop_remainder=True).map(
    lambda x, y: preprocess_data(x, y, augment=True),
    num_parallel_calls=tf.data.AUTOTUNE).prefetch(
    tf.data.AUTOTUNE)

# Create a model using a pretrained backbone from keras-cv
backbone = keras_cv.models.EfficientNetV2Backbone.from_preset(
    "efficientnetv2_b0_imagenet"
) # use EfficientNetV2Backbone from keras-cv
model = keras_cv.models.ImageClassifier(
    backbone=backbone,
    num_classes=NUM_CLASSES,
    activation="softmax",
) # use ImageClassifier from keras-cv

model.compile(
    loss='categorical_crossentropy',
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
    metrics=['accuracy']
)

# Train your model
model.fit(
    train_dataset,
    epochs=8,
)

# Use the trained model to interpolate new frames between the existing frames in the video.
output_frames = []
for i in range(len(frames) - 1):
    prev_frame = frames[i]
    next_frame = frames[i + 1]

    # Generate the next frame
    prediction = model.predict(np.expand_dims(prev_frame, axis=0))

    # Create the output frame
    output_frame = np.concatenate([prev_frame, prediction], axis=1)

    output_frames.append(output_frame)

# Save the output video.
cv2.VideoWriter('./output/output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (frames[0].shape[1], frames[0].shape[0])).writeframes(output_frames)
