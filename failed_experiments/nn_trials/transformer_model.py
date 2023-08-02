import torch
import torch.nn as nn
import torch.optim as optim
import torch.cuda.amp as amp


class TransformerFrameInterpolation(nn.Module):
    def __init__(self):
        super().__init__()
        # The embedding layer transforms the input frames into shallow features.
        self.embedding = nn.Embedding(2, 64)
        # The Transformer encoder-decoder network extracts deep hierarchical features from the input frames.
        self.encoder = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=64, nhead=8),
            num_layers=6,
        )
        self.decoder = nn.TransformerDecoder(
            nn.TransformerDecoderLayer(d_model=64, nhead=8),
            num_layers=6,
        )
        # The multi-scale frame synthesis network synthesizes the interpolated frames.
        self.synthesis = nn.ModuleList([
            nn.Conv2d(64, 64, 3, stride=1, padding=1),
            nn.Conv2d(64, 64, 3, stride=1, padding=1),
            nn.Conv2d(64, 3, 3, stride=1, padding=1),
        ])

    def forward(self, frames):
        # Concatenate the frames in the batch into a single tensor.
        frames = torch.cat(frames, dim=0)
        # Transfer the input frames to the device.
        frames = frames.to(device)
        # Round the values in the frames tensor and convert it to a long tensor.
        frames = torch.round(frames).long()
        # The embedding layer transforms the input frames into shallow features.
        features = self.embedding(frames)
        features = features.unsqueeze(0)
        # Reshape the features tensor to have an embedding dimension of 64.
        features = torch.reshape(features, (-1, 64)) # Added this line
        # The Transformer encoder-decoder network extracts deep hierarchical features from the input frames.
        encoded_features = self.encoder(features.unsqueeze(0)).squeeze(0)
        # The multi-scale frame synthesis network synthesizes the interpolated frames.
        interpolated_frames = []
        for level in range(3):
            output = self.synthesis[level](encoded_features)
            interpolated_frames.append(output)

        return interpolated_frames

def train(model, train_loader, val_loader, loss_fn, optimizer, epochs):
    scaler = amp.GradScaler()
    for epoch in range(epochs):
        print("Epoch:", epoch)
        for i, batch in enumerate(train_loader):
            # Get the input frames.
            frames = batch["frames"]
            tuple(t.to(device) for t in frames)
            # Forward pass.
            output_frames = model(frames)
            tuple(t.to(device) for t in frames)
            # Calculate the loss.
            loss = loss_fn(output_frames, batch["target_frames"])
            # Backpropagate the loss.
            optimizer.zero_grad()
            # Forward pass
            with amp.autocast():  # Use autocast context manager
                output_frames = model(frames)
                loss = loss_fn(output_frames, output_frames)
            # Backward pass
            scaler.scale(loss).backward()  # Use scaler methods
            scaler.step(optimizer)
            scaler.update()
            # # Update the model parameters.
            # optimizer.step()
        # Evaluate the model on the validation set.
        val_loss = 0
        for batch in val_loader: # Changed this line
            # Get the input frames.
            frames = batch["frames"]
            frames.to(device)
            # Resize the images to 640x480x24.
            frames = frames.resize(640, 480, 24)
            # Forward pass.
            output_frames = model(frames)
            # Calculate the loss.
            loss = loss_fn(output_frames, batch["target_frames"])
            val_loss += loss.item()
        val_loss /= len(val_loader) # Changed this line
        print(f"Epoch {epoch + 1}, validation loss: {val_loss}")
    torch.save(model, "model.pt")

if __name__ == "__main__":
    # Load the dataset.
    dataset = torch.load("data_reduced.pt")

    # Split the dataset into training and validation sets.
    train_dataset, val_dataset = torch.utils.data.random_split(dataset, [0.8, 0.2])
    # Create data loaders for the training and validation sets. # Added this line
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=2, collate_fn=lambda x: {"frames": x[0], "target_frames": x[1]})
    val_loader = torch.utils.data.DataLoader(val_dataset, batch_size=2, collate_fn=lambda x: {"frames": x[0], "target_frames": x[1]})

    # Train the model.
    model = TransformerFrameInterpolation()
    loss_fn = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    torch.cuda.empty_cache()
    device = torch.device('cuda')
    import torch

    if torch.cuda.is_available():
        print("CUDA is available")
    else:
        print("CUDA is not available")
    # Transfer the model to the device.
    model.to(device)
    train(model, train_loader, val_loader, loss_fn, optimizer, 10)