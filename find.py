import json

def load_json_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def search_phone_numbers(data, phone_numbers):
    found = {}
    not_found = []

    for number in phone_numbers:
        number = number.strip()
        matched = False
        for username, numbers in data.items():
            if number in numbers:
                found[number] = username
                matched = True
                break
        if not matched:
            not_found.append(number)

    return found, not_found

def main():
    filename = 'extracted_phone_numbers.json'
    data = load_json_data(filename)

    input_numbers = input("Enter phone numbers separated by commas: ")
    phone_numbers = input_numbers.split(',')

    found, not_found = search_phone_numbers(data, phone_numbers)

    print("\nFound Phone Numbers and Usernames:")
    for number, username in found.items():
        print(f"{number} => {username}")

    if not_found:
        print("\nPhone Numbers Not Found:")
        for number in not_found:
            print(number)

if __name__ == "__main__":
    main()
