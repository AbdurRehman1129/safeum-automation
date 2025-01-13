import json

def get_phone_numbers(file_path, usernames):
    try:
        # Load the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Process the input usernames
        username_list = [username.strip() for username in usernames.split(",")]
        phone_numbers = []
        
        # Fetch phone numbers for the provided usernames
        for username in username_list:
            if username in data:
                # Remove spaces from the phone number
                phone_number = data[username][0].replace(" ", "")
                phone_numbers.append(phone_number)
            else:
                print(f"Username '{username}' not found. Skipping...")
        
        # Return the comma-separated phone numbers
        return ",".join(phone_numbers)
    except Exception as e:
        return f"An error occurred: {e}"

# Main code
if __name__ == "__main__":
    # Path to the JSON file
    file_path = "extracted_phone_numbers.json"
    
    # Ask for usernames
    input_usernames = input("Enter usernames separated by comma: ")
    
    # Get phone numbers
    result = get_phone_numbers(file_path, input_usernames)
    
    if result:
        print(f"Phone Numbers: {result}")
    else:
        print("No phone numbers found.")
