import re
models = ['1024']

list_files = []
for model in models:
    st = "output_alexnet_"+model+".txt"
    list_files.append(st)

values = []

for file_name in list_files:
    with open(file_name, "r") as input_file:
        pattern = r"Compute time is (\d+\.\d+)"
        content = input_file.read()
        # Use re.search() to find the pattern in the input string
        matches = re.findall(pattern, content)

        # Convert the matched strings to integers and return as a list
        numbers = [float(match) for match in matches]
        values=numbers

# Open a new file for writing
with open("parsed_output_alexnet.txt", "a") as output_file:
    for value in values:
        output_file.write(str(value) + "\n")
