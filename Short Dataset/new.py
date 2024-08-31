import csv
import json
import os
from tqdm import tqdm

def get_paths():
    csv_file_path = input("Enter the path to your CSV file: ").strip()
    exploit_folder_path = input("Enter the path to your folder with exploit files: ").strip()
    json_output_path = input("Enter the path to save the output JSON file (including the filename): ").strip()
    return csv_file_path, exploit_folder_path, json_output_path

def load_csv_data(csv_file_path):
    with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
        return list(csv.DictReader(csvfile))

def get_exploit_code(exploit_folder_path, exploit_id):
    file_extensions = ['.py', '.c', '.rb', '.txt']  # Add more if needed
    for ext in file_extensions:
        file_path = os.path.join(exploit_folder_path, f'{exploit_id}{ext}')
        if os.path.exists(file_path):
            with open(file_path, mode='r', encoding='utf-8') as exploitfile:
                return exploitfile.read()
    return None

def create_json_entry(row, exploit_code):
    return {
        "instruction": "Provide detailed information about the given exploit.",
        "input": f"Exploit ID: {row['id']}",
        "output": {
            "ID": row['id'],
            "Description": row['description'],
            "Date Published": row['date_published'],
            "Author": row['author'],
            "Platform": row['platform'],
            "Codes": row['codes'].split(','),
            
        }
    }

def save_json_data(json_data, json_output_path):
    with open(json_output_path, mode='w', encoding='utf-8') as jsonfile:
        json.dump(json_data, jsonfile, indent=4)

def main():
    csv_file_path, exploit_folder_path, json_output_path = get_paths()
    csv_data = load_csv_data(csv_file_path)
    json_data = []

    # Initialize progress bar
    print("Processing the exploits and creating JSON dataset:")
    with tqdm(total=len(csv_data), ascii=True, desc="Progress") as pbar:
        for row in csv_data:
            exploit_id = row['id']
            exploit_code = get_exploit_code(exploit_folder_path, exploit_id)
            if exploit_code is not None:
                json_entry = create_json_entry(row, exploit_code)
                json_data.append(json_entry)
            else:
                print(f"\nWarning: No exploit file found for ID {exploit_id}. Skipping this entry.")
            
            # Update progress bar
            pbar.update(1)

    save_json_data(json_data, json_output_path)
    print(f"\nJSON dataset creation complete! Saved to {json_output_path}")

if __name__ == "__main__":
    main()
