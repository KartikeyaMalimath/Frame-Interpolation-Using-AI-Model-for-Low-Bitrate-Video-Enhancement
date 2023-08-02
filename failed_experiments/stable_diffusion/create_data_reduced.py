import os

import torch
from PIL import Image
from torchvision import transforms

def create_data_reduced(data_dir, output_file, resize):
    """
    Create a PyTorch dataset of resized images.

    Args:
        data_dir: The directory containing the images.
        output_file: The path to the output file.
        resize: The size to resize the images to.
    """
    # Create a list of all the images in the data directory.
    images = os.listdir(data_dir)
    # Create a dataset of PIL images.
    dataset = []
    for image in images:
        image = os.path.join(data_dir, image)
        image = Image.open(image)
        image = image.resize(resize)
        dataset.append(image)
    # Convert the dataset to a PyTorch dataset.
    dataset = torch.utils.data.TensorDataset(torch.stack([transforms.ToTensor()(image) for image in dataset]))
    # Save the dataset to the output file.
    torch.save(dataset, output_file)

if __name__ == "__main__":
    data_dir = "../../data/"
    output_file = "data_reduced.pt"
    resize = (640, 480)
    create_data_reduced(data_dir, output_file, resize)