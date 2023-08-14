import re
models = ['256']

list_files = []
for model in models:
    st = "output"+model+".txt"
    list_files.append(st)

values_A = []

for file_name in list_files:
    with open(file_name, "r", encoding="latin-1") as input_file:
        pattern_A = r"Time taken by thread_main is : (\d+\.\d+)"
        content = input_file.read()
        # Use re.search() to find the pattern in the input string
        matches_A = re.findall(pattern_A, content)
        # Convert the matched strings to integers and return as a list
        values_A=[float(match) for match in matches_A]
    
# Open a new file for writing
with open("parsed_output.txt", "a", encoding="latin-1") as output_file:
    for val in values_A:
        output_file.write(str(val) + "\n")



