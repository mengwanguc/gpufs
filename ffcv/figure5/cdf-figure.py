import numpy as np
import matplotlib.pyplot as plt

# data1 = np.random.randn(1000)  # Sample data for line 1
# data2 = np.random.randn(1000) + 1  # Sample data for line 2 (offset for illustration)

# Initialize an empty list to store the numbers
run_gpu_list = []

# Open the file in read mode
with open('run-gpu-time-final.txt', 'r') as file:
    # Read and convert each line to a floating-point number
    for line in file:
        line = line.strip()  # Remove leading/trailing whitespace
        if line:  # Check if the line is not empty
            try:
                number = float(line)  # Convert the line to a float
                run_gpu_list.append(number)  # Append the number to the list
            except ValueError:
                print(f"Warning: Skipped line '{line}' as it is not a valid float.")

# Initialize an empty list to store the numbers
run_cpu_list = []

# Open the file in read mode
with open('run-cpu-time-final.txt', 'r') as file:
    # Read and convert each line to a floating-point number
    for line in file:
        line = line.strip()  # Remove leading/trailing whitespace
        if line:  # Check if the line is not empty
            try:
                number = float(line)  # Convert the line to a float
                run_cpu_list.append(number)  # Append the number to the list
            except ValueError:
                print(f"Warning: Skipped line '{line}' as it is not a valid float.")

# Initialize an empty list to store the numbers
# totorchimage_list = []

# # Open the file in read mode
# with open('totorchimage.txt', 'r') as file:
#     # Read and convert each line to a floating-point number
#     for line in file:
#         line = line.strip()  # Remove leading/trailing whitespace
#         if line:  # Check if the line is not empty
#             try:
#                 number = float(line)  # Convert the line to a float
#                 # print(number)
#                 totorchimage_list.append(number)  # Append the number to the list
#             except ValueError:
#                 print(f"Warning: Skipped line '{line}' as it is not a valid float.")


# # Initialize an empty list to store the numbers
# convert_list = []

# # Open the file in read mode
# with open('convert.txt', 'r') as file:
#     # Read and convert each line to a floating-point number
#     for line in file:
#         line = line.strip()  # Remove leading/trailing whitespace
#         if line:  # Check if the line is not empty
#             try:
#                 number = float(line)  # Convert the line to a float
#                 convert_list.append(number)  # Append the number to the list
#             except ValueError:
#                 print(f"Warning: Skipped line '{line}' as it is not a valid float.")
  

# Sort the data
data1_sorted = np.sort(run_gpu_list)
data2_sorted = np.sort(run_cpu_list)
# data3_sorted = np.sort(totorchimage_list)
# data4_sorted = np.sort(convert_list)

# Calculate the CDF values
cdf1 = np.arange(1, len(data1_sorted) + 1) / len(data1_sorted)
cdf2 = np.arange(1, len(data2_sorted) + 1) / len(data2_sorted)
# cdf3 = np.arange(1, len(data2_sorted) + 1) / len(data3_sorted)
# cdf4 = np.arange(1, len(data2_sorted) + 1) / len(data4_sorted)

plt.figure(figsize=(8, 4))  # Set the figure size (optional)
plt.xlim([0, 0.0004])
plt.plot(data1_sorted, cdf1, label="run_gpu")  # Plot CDF for line 1
plt.plot(data2_sorted, cdf2, label="run_cpu")  # Plot CDF for line 2
# plt.plot(data3_sorted, cdf3, label="totorchimage", linewidth=3, linestyle='dashed')  # Plot CDF for line 2
# plt.plot(data3_sorted, cdf4, label="convert")  # Plot CDF for line 2

# Customize the chart with labels, legend, etc.
plt.xlabel("X-axis Label")
plt.ylabel("CDF")
plt.title("CDF Plot ")
plt.legend()

plt.grid(True)  # Add grid lines (optional)

# plt.show()  # Display the chart

plt.savefig("cdf-figure-fig5.jpg", format="jpg")