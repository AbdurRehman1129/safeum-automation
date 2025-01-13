import json

# Load the data from the JSON file
with open("extracted_phone_numbers.json", "r") as file:
    data = json.load(file)

# Reverse the data structure for faster lookup
number_to_username = {}
for username, numbers in data.items():
    for number in numbers:
        clean_number = number.replace(" ", "")  # Remove spaces for lookup
        number_to_username[clean_number] = username

# Function to search usernames by numbers
def search_usernames(numbers):
    numbers = [num.strip() for num in numbers.split(",")]  # Handle multiple numbers
    results = {}
    for num in numbers:
        if num in number_to_username:
            results[num] = number_to_username[num]
        else:
            results[num] = "Not Found"
    return results

# Input from the user
user_input = input("Enter number(s) (comma-separated without spaces): ")

# Perform the search
result = search_usernames(user_input)

# Print the results
for number, username in result.items():
    print(f"Number: {number}, Username: {username}")
