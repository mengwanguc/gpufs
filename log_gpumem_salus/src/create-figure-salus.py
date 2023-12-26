import matplotlib.pyplot as plt

# Read data from fps_log.txt and time_log.txt
with open("fps_log1.txt", "r") as fps_file:
    fps_data1 = [float(line.strip()) for line in fps_file.readlines()]

with open("time_log1.txt", "r") as time_file:
    time_data1 = [float(line.strip()) for line in time_file.readlines()]

# Read data from fps_log.txt and time_log.txt
with open("fps_log2.txt", "r") as fps_file:
    fps_data2 = [float(line.strip()) for line in fps_file.readlines()]

with open("time_log2.txt", "r") as time_file:
    time_data2 = [float(line.strip()) for line in time_file.readlines()]

# Read data from fps_log.txt and time_log.txt
with open("fps_log3.txt", "r") as fps_file:
    fps_data3 = [float(line.strip()) for line in fps_file.readlines()]

with open("time_log3.txt", "r") as time_file:
    time_data3 = [float(line.strip()) for line in time_file.readlines()]

# Plotting the line graph
plt.plot(time_data1, fps_data1, linestyle='-')
plt.plot(time_data2, fps_data2, linestyle='-')
plt.plot(time_data3, fps_data3, linestyle='-')
# plt.plot(time_data, fps_data , linestyle='-')
plt.title('Time vs. Image per second')
plt.xlabel('Time (seconds)')
plt.ylabel('Image per seconds')
plt.grid(True)
# plt.show()

plt.savefig("salus-fig.jpg", format="jpg")
