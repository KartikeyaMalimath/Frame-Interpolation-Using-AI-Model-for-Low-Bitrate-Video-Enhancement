import tensorflow as tf

devices = tf.config.list_physical_devices("GPU")

tf.config.set_visible_devices(devices[0])
if devices:
  print("GPU is available")
else:
  print("GPU is not available")