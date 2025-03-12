import os
import json
import pandas as pd
import platform

# Define filename
filename = "Extracted_Phone_numbers.xlsx"

# Load JSON file
def load_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

# Save data to Excel
def save_to_excel(data, save_dir):
    df = pd.DataFrame([(key, num) for key, numbers in data.items() for num in numbers], columns=["Username", "Phone Number"])
    
    # Ensure unique filename
    base_name, ext = os.path.splitext(filename)
    file_path = os.path.join(save_dir, filename)
    count = 1
    while os.path.exists(file_path):
        file_path = os.path.join(save_dir, f"{base_name}_{count}{ext}")
        count += 1
    
    # Save the file
    df.to_excel(file_path, index=False)
    print(f"File saved at: {file_path}")

# Check if running on Termux
def is_termux():
    return "com.termux" in os.getenv("PREFIX", "")

# Ensure Termux storage access
def check_termux_storage():
    storage_path = "/data/data/com.termux/files/home/storage/shared/Safeum Numbers"
    if not os.path.exists(storage_path):
        print("Termux storage not accessible. Run: termux-setup-storage and restart script.")
        exit(1)
    return storage_path

# Main function
def main():
    json_file = "extracted_phone_numbers.json"
    if not os.path.exists(json_file):
        print("JSON file not found!")
        return

    data = load_json(json_file)
    
    if is_termux():
        save_dir = check_termux_storage()
    else:
        save_dir = os.path.dirname(os.path.abspath(__file__))
    
    save_to_excel(data, save_dir)

if __name__ == "__main__":
    main()
