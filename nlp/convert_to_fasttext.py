import pandas as pd
import json
import bz2

# Path to the JSON file containing the reviews data
input_file_path = "Gift_Cards.json"

# Read the JSON file and parse each review as a separate dictionary
data = []
with open(input_file_path, 'r') as file:
    for line in file:
        review = json.loads(line.strip())
        data.append(review)

# Create a DataFrame from the list of dictionaries
reviews_df = pd.DataFrame(data)

print(reviews_df.head())  # Display the first few rows of the DataFrame
print(type(reviews_df))  # Display the first few rows of the DataFrame


# Function to assign labels based on overall ratings
def assign_label(row):
    if row['overall'] in (1, 2):
        return int(1)
    elif row['overall'] in (4, 5):
        return int(2)

# Add the 'label' column based on overall ratings
reviews_df['label'] = reviews_df.apply(assign_label, axis=1)
print(type(reviews_df['label'][0]))
reviews_df.dropna(subset=['label'], inplace=True)
reviews_df['label'] = reviews_df['label'].astype(int)
print(type(reviews_df['label'][0]))

print(reviews_df.head())  # Display the first few rows of the DataFrame with the new 'label' colu

# Create FastText formatted lines with label and reviewText
# fasttext_lines = reviews_df.apply(lambda row: f"{row['label']} {row['reviewText']}\n", axis=1)

# # Path to the FastText formatted output file
# output_file_path = "output_file.txt.bz2"

# # Save the FastText formatted lines to the .txt.bz2 file
# with bz2.BZ2File(output_file_path, 'w') as f:
#     f.writelines(line.encode('utf-8') for line in fasttext_lines)

# print("Conversion completed. FastText formatted file saved as .txt.bz2")


# Sample DataFrame
# data = {'label': ['positive', 'negative', 'neutral'],
#         'text': ['This is a positive review', 'This is a negative review', 'This is a neutral review']}
# df = pd.DataFrame(data)

reviews_df['reviewText'] = reviews_df['reviewText'].str.replace('\n', '\\n')

df = reviews_df

# Convert DataFrame to FastText data format
fasttext_data = []
for index, row in df.iterrows():
    label = row['label']
    text = row['reviewText']
    fasttext_data.append(f"__label__{label} {text}")

# Save the FastText data to a text file
with open('fasttext_data.txt', 'w') as f:
    f.write('\n'.join(fasttext_data))

# # Path to the FastText formatted output file
output_file_path = "output_file.txt.bz2"

print(fasttext_data[0])
print(fasttext_data[1])

# # Save the FastText formatted lines to the .txt.bz2 file
with bz2.BZ2File(output_file_path, 'w') as f:
    f.writelines(line.encode('utf-8') for line in fasttext_data)

print("Conversion completed. FastText formatted file saved as .txt.bz2")

