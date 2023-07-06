import torch
import torch.nn as nn
from dall_e import DALLE

class ModifiedDALLEModel(DALLE):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.encoder.input_channels = 4
        self.decoder.input_channels = 4

# Create an instance of the modified DALL-E model
dalle_model = ModifiedDALLEModel()

# Load pre-trained weights
pretrained_weights_path = "path/to/pretrained/model.pt"
dalle_model.load_state_dict(torch.load(pretrained_weights_path))

# Example usage
batch_size = 1
input_channels = 4
input_shape = (batch_size, input_channels, 256, 256)  # Specify the desired input shape
input_tensor = torch.randn(input_shape)

output = dalle_model(input_tensor)
print(output.shape)
