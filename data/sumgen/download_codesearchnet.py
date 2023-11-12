from datasets import load_dataset
import os
import json

# Load the 'python' part of the code_search_net dataset

# Define the base directory where the files will be saved
base_dir = "."  # Replace with your desired path

# Create the base directory
os.makedirs(base_dir, exist_ok=True)

# Define the mapping from original to expected column names
column_mapping = {
    'repository_name': 'repo',
    'func_path_in_repository': 'path',
    'func_name': 'func_name',
    'whole_func_string': 'original_string',
    'language': 'language',
    'func_code_string': 'code',
    'func_code_tokens': 'code_tokens',
    'func_documentation_string': 'docstring',
    'func_documentation_tokens': 'docstring_tokens',  # Corrected here
    'split_name': 'partition',
    'func_code_url': 'url'
}

LANGUAGES = ["python", "java"]

for language in LANGUAGES:
    dataset = load_dataset("code_search_net", language)
    save_dir = os.path.join(base_dir, language)
    os.makedirs(save_dir, exist_ok=True)

    for split in dataset.keys():
        # Define the jsonl file path
        jsonl_file_path = os.path.join(save_dir, f"{split}.jsonl")

        # Open the file for writing
        with open(jsonl_file_path, 'w') as jsonl_file:
            # Iterate through each record in the split
            for record in dataset[split]:
                # Map the dataset columns to the expected columns
                mapped_record = {new_key: record[old_key] for old_key, new_key in column_mapping.items()}
                # Add additional fields if necessary
                mapped_record['sha'] = 'N/A'  # Replace with actual data if available
                # Write the mapped record to the jsonl file
                jsonl_file.write(json.dumps(mapped_record) + '\n')

    print(f"Dataset for {language} saved in directory: {save_dir}")

# V1
# from datasets import load_dataset
# import os

# # Load the 'python' part of the code_search_net dataset

# # Define the base directory where the files will be saved
# base_dir = "."  # Replace with your desired path

# # Create the base directory
# os.makedirs(base_dir, exist_ok=True)

# # Save each split of the dataset in jsonl format

# LANGUAGES = ["python", "java"]

# for language in LANGUAGES:
#     dataset = load_dataset("code_search_net", language)
#     save_dir = os.path.join(base_dir, language)
#     for split in dataset.keys():
#         # Define the directory for each split
#         # split_dir = os.path.join(base_dir, split)
#         # os.makedirs(split_dir, exist_ok=True)

#         # Define the jsonl file path
#         jsonl_file_path = os.path.join(save_dir, f"{split}.jsonl")

#         # Convert the dataset split to jsonl and save to file
#         dataset[split].to_json(jsonl_file_path)

#     print(f"Dataset saved in directory: {base_dir}")
