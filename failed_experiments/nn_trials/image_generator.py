import keras_cv
from matplotlib import pyplot as plt

model = keras_cv.models.StableDiffusion(img_width=512, img_height=512)

prompt = "A cat sitting on a couch"

image = model.generate_image(prompt)

plt.imshow(image)
plt.show()
