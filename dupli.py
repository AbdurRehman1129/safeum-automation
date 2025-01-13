import json
from collections import defaultdict

# Load JSON data from the file
with open("extracted_phone_numbers.json", "r") as file:
    data = json.load(file)

# Flatten phone numbers into a single list
phone_to_keys = defaultdict(list)

for key, phone_numbers in data.items():
    for phone in phone_numbers:
        phone_to_keys[phone].append(key)

# Find duplicates
duplicates = {phone: keys for phone, keys in phone_to_keys.items() if len(keys) > 1}

# Display results
if duplicates:
    print("Duplicate phone numbers found:")
    for phone, keys in duplicates.items():
        print(f"Phone: {phone}, Found in keys: {keys}")
else:
    print("No duplicate phone numbers found.")
