import subprocess
import json

# Replace 'script1.py' and 'script2.py' with your script filenames
script1 = 'alexnet-salus-1.py'
script2 = 'alexnet-salus-1.py'

# Number of iterations or epochs
num_iterations = 10

for i in range(num_iterations):
    print(f"Training iteration {i + 1}")
    with open('/home/cc/gpufs/log_gpumem_salus/src/edev/egpu0.json', 'r') as file:
        json_data = file.read()

    print("json-data ->",json_data)
    egpu = json.loads(json_data)
    print(egpu)

    # Run script 1
    if egpu["occupied"] == False:
        process1 = subprocess.Popen(['python', script1])
        process1.wait()

    # Run script 2
    if egpu["occupied"] == False:
        process2 = subprocess.Popen(['python', script2])
        process2.wait()

    # Optional: Add a delay or sleep between iterations
    # time.sleep(1)
