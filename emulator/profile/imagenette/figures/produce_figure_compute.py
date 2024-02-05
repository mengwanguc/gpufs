import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Generate some sample data
batch_sizes = [1,2,3,4,5,6,7,8,9,10,
                11,12,13,14,15,16,17,18,19,20,
                21,22,23,24,25,26,27,28,29,30,
                31,32,64,128,256]

csv_file_path = 'alexnet-compute.csv'
df = pd.read_csv(csv_file_path, header=None, names=['Value'])
model1_times = df['Value'].tolist()
print(model1_times)

csv_file_path = 'resnet18-compute.csv'
df = pd.read_csv(csv_file_path, header=None, names=['Value'])
model2_times = df['Value'].tolist()
print(model2_times)

csv_file_path = 'mobilenet-compute.csv'
df = pd.read_csv(csv_file_path, header=None, names=['Value'])
model3_times = df['Value'].tolist()
print(model3_times)


# Create the plot
plt.figure(figsize=(10, 6))

# Plot each model's performance
plt.plot(batch_sizes, model1_times, label='Alexnet', marker='o')
plt.plot(batch_sizes, model2_times, label='Resnet18', marker='s')
plt.plot(batch_sizes, model3_times, label='Mobilenetv2', marker='^')

# Add labels and title
plt.xlabel('Batch Size')
plt.ylabel('Time (seconds)')
plt.title('Model Performance vs. Batch Size')
plt.legend()

# Show the plot
plt.grid(True)
# plt.show()

plt.savefig("figure-compute.jpg", format="jpg")
