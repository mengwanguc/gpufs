import matplotlib.pyplot as plt

# Read data from fps_log.txt and time_log.txt
with open("fps_log.txt", "r") as fps_file:
    fps_data = [float(line.strip()) for line in fps_file.readlines()]

with open("time_log.txt", "r") as time_file:
    time_data = [float(line.strip()) for line in time_file.readlines()]

# Plotting the line graph
plt.plot(time_data, fps_data , marker='o', linestyle='-')
# plt.plot(time_data, fps_data , linestyle='-')
plt.title('Time vs. Image per second')
plt.xlabel('Time (seconds)')
plt.ylabel('Image per seconds')
plt.grid(True)
# plt.show()

plt.savefig("salus-fig.jpg", format="jpg")
