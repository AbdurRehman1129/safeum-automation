import re

def extract_and_format_phone_numbers(text):
    # Define a regex pattern to match phone numbers starting with 9944, allowing spaces in between digits
    pattern = r"9944[ \d]{8,}"  # Matches '9944' followed by 10 or more spaces/digits
    
    # Find all matching phone numbers
    matches = re.findall(pattern, text)
    
    # Clean phone numbers: Remove spaces and '+' if present
    cleaned_numbers = [re.sub(r"[ +]", "", match) for match in matches]
    
    # Join the numbers with commas
    result = ",".join(cleaned_numbers)
    return result

# Input text from the user
print("Enter the text containing phone numbers (press Enter twice to finish):")
lines = []
while True:
    line = input()
    if line.strip() == "":
        break
    lines.append(line)
text = "\n".join(lines)

# Extract and format phone numbers
formatted_numbers = extract_and_format_phone_numbers(text)

# Output the result
if formatted_numbers:
    print("Formatted Phone Numbers:", formatted_numbers)
else:
    print("No valid phone numbers found in the text.")
