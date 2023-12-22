import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import time

# Define the AlexNet architecture
class AlexNet(nn.Module):
    def __init__(self, num_classes=10):
        super(AlexNet, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=11, stride=4, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
            nn.Conv2d(64, 192, kernel_size=5, padding=2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
            nn.Conv2d(192, 384, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(384, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
        )
        self.avgpool = nn.AdaptiveAvgPool2d((6, 6))
        self.classifier = nn.Sequential(
            nn.Dropout(),
            nn.Linear(256 * 6 * 6, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Linear(4096, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), 256 * 6 * 6)
        x = self.classifier(x)
        return x

# Dummy dataset class for testing
class DummyDataset(Dataset):
    def __init__(self, num_samples=1000):
        self.data = torch.randn((num_samples, 3, 224, 224))
        self.labels = torch.randint(0, 10, (num_samples,))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]

# Instantiate AlexNet and create a dummy dataset
alexnet = AlexNet(num_classes=10)
dummy_dataset = DummyDataset(num_samples=1000)

# DataLoader for the dummy dataset
batch_size = 32
data_loader = DataLoader(dummy_dataset, batch_size=batch_size, shuffle=True)

# Define loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(alexnet.parameters(), lr=0.001)

# Initialize variables for logging
log_interval = 1  # Log every second
current_second = 0
fps_log = []
time_log = []

# Training loop
num_epochs = 5
iteration = 1

start_time_log = time.time()
for epoch in range(num_epochs):
    for batch in data_loader:
        inputs, labels = batch

        # Measure the time taken for each iteration
        start_time = time.time()

        # Forward pass, backward pass, and optimization
        optimizer.zero_grad()
        outputs = alexnet(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        end_time = time.time()

        # Calculate FPS
        time_per_iteration = end_time - start_time
        fps = 1 / time_per_iteration

        # Log FPS and time every second
        if int(end_time) > current_second:
            fps_log.append(round(fps, 0))
            time_log.append(end_time - start_time_log)
            current_second += 1

        # Print some information
        if iteration % log_interval == 0:
            print(f"Epoch: {epoch+1}, Iteration: {iteration}, Loss: {loss.item():.4f}, FPS: {fps:.2f}")

        iteration += 1

# Save the logs to text files
with open("fps_log.txt", "w") as fps_file:
    for fps in fps_log:
        fps_file.write(f"{fps:.2f}\n")

with open("time_log.txt", "w") as time_file:
    for timestamp in time_log:
        time_file.write(f"{timestamp}\n")
