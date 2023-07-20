import re
models = ['shufflenet_v2_x0_5','alexnet','resnet18','squeezenet1_0','squeezenet1_1','mobilenet_v2','resnet50','vgg11']

list_files = []
for model in models:
    st = "output_100"+model+".txt"
    list_files.append(st)

values = []
for file_name in list_files:
    with open(file_name, "r") as input_file:
        lines = input_file.readlines()
        last_two_lines = lines[-1:]
        for line in last_two_lines:
            values.append(line.strip())

# Open a new file for writing
with open("parsed_output_100.txt", "a") as output_file:
    for value in values:
        output_file.write(str(value) + "\n")
