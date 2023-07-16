import os
import cv2
import torch
from torch.utils.data import Dataset

class FramesDataset(Dataset):
    def __init__(self, frames_directory, transform=None):
        self.frames_directory = frames_directory
        self.frames = sorted(os.listdir(frames_directory))
        self.transform = transform

    def __len__(self):
        return len(self.frames)

    def __getitem__(self, idx):
        frame_path = os.path.join(self.frames_directory, self.frames[idx])
        frame = cv2.imread(frame_path)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB

        if self.transform:
            frame = self.transform(frame)

        return frame

if __name__ == "__main__":
    frames_directory = "path/to/frames/directory"
    dataset = FramesDataset(frames_directory)
    # Create a data loader
    batch_size = 16
    data_loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)
