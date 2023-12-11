import matplotlib.pyplot as plt
import numpy as np

# Updated batch sizes
batch_sizes = [1, 2, 3, 4, 5, 6, 64, 128, 256]

model1_times = [10, 15, 25, 40, 60, 80, 100, 120, 150]
model2_times = [8, 12, 20, 32, 48, 64, 80, 100, 120]
model3_times = [12, 18, 30, 45, 70, 90, 110, 130, 160]

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))

# Plot each model's performance
ax.plot(batch_sizes, model1_times, label='Model 1', marker='o')
ax.plot(batch_sizes, model2_times, label='Model 2', marker='s')
ax.plot(batch_sizes, model3_times, label='Model 3', marker='^')

# Add labels and title
ax.set_xlabel('Batch Size')
ax.set_ylabel('Time (seconds)')
ax.set_title('Model Performance vs. Batch Size')

# Add legend
ax.legend()

# Create a broken axis
ax.set_xscale('linear')
ax.spines['bottom'].set_linestyle((0, (5, 2)))
ax.spines['top'].set_linestyle((0, (5, 2)))
ax.spines['right'].set_linestyle((0, (5, 2)))

# Set x-axis ticks manually for a fixed distance
tick_positions = np.arange(min(batch_sizes), max(batch_sizes) + 1, step=32)
ax.set_xticks(tick_positions)

# Show the plot
plt.grid(True)
plt.show()

# Save the plot as a JPEG file
plt.savefig("figure1.jpg", format="jpg")
