import time
import torch
import argparse
from torchvision.models import resnet18

def measure_per_batch_time(num_gpus, batch_size):
    """Function to measure per-batch training time in DP for ResNet-18."""
    if torch.cuda.device_count() < num_gpus:
        print(f"Error: Requested {num_gpus} GPUs, but only {torch.cuda.device_count()} are available.")
        return

    # Create the model and wrap it with DP
    model = resnet18()
    model = torch.nn.DataParallel(model, device_ids=list(range(num_gpus)))
    model = model.cuda()

    # Generate dummy data and preload it to the GPU
    input_data = torch.randn(batch_size, 3, 224, 224).cuda()
    labels = torch.randint(0, 1000, (batch_size,)).cuda()

    # Set up criterion and optimizer
    criterion = torch.nn.CrossEntropyLoss().cuda()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

    # Measure time for each batch
    num_iterations = 10

    for i in range(num_iterations):
        # Synchronize before starting the batch to ensure all previous work is done
        torch.cuda.synchronize()
        batch_start = time.time()

        # Forward, backward, and optimizer step
        optimizer.zero_grad()
        outputs = model(input_data)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        # Synchronize after completing the batch to ensure all GPU work is done
        torch.cuda.synchronize()
        batch_end = time.time()

        # Print time for this batch
        print(f"Batch {i + 1}: {batch_end - batch_start:.4f} seconds with {num_gpus} GPUs and batch size {batch_size}")

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="DP Per-Batch Timing Test with ResNet-18 and Custom Batch Size")
    parser.add_argument(
        "--gpus", type=int, required=True, help="Number of GPUs to use for DP"
    )
    parser.add_argument(
        "--batch_size", type=int, required=True, help="Custom batch size"
    )
    args = parser.parse_args()

    num_gpus = args.gpus
    batch_size = args.batch_size

    # Run the timing test
    measure_per_batch_time(num_gpus, batch_size)

if __name__ == "__main__":
    main()
