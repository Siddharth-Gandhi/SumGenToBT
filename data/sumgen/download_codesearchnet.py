# from datasets import load_dataset
# import os
# import shutil

# def download_and_zip_dataset():
#     # Load the dataset
#     ds = load_dataset("code_search_net", "python")

#     # Define the directory to save the files
#     save_dir = "python_code_search_net"
#     os.makedirs(save_dir, exist_ok=True)

#     # Save the dataset to the directory
#     ds.save_to_disk(save_dir)

#     # Create a ZIP file from the saved directory
#     shutil.make_archive("python", 'zip', save_dir)

# if __name__ == "__main__":
#     download_and_zip_dataset()

from datasets import load_dataset
import os

# Load the 'python' part of the code_search_net dataset

# Define the base directory where the files will be saved
base_dir = "."  # Replace with your desired path

# Create the base directory
os.makedirs(base_dir, exist_ok=True)

# Save each split of the dataset in jsonl format

LANGUAGES = ["python", "java"]

for language in LANGUAGES:
    dataset = load_dataset("code_search_net", language)
    save_dir = os.path.join(base_dir, language)
    for split in dataset.keys():
        # Define the directory for each split
        # split_dir = os.path.join(base_dir, split)
        # os.makedirs(split_dir, exist_ok=True)

        # Define the jsonl file path
        jsonl_file_path = os.path.join(save_dir, f"{split}.jsonl")

        # Convert the dataset split to jsonl and save to file
        dataset[split].to_json(jsonl_file_path)

    print(f"Dataset saved in directory: {base_dir}")
