import sys

# Prompt the user to paste all username:password pairs
print("Paste all username:password pairs below (press Enter, then Ctrl+D on Linux/Mac or Ctrl+Z on Windows when done):")

# Read input from the user
input_text = sys.stdin.read().strip()

# Process the input to extract usernames only
usernames = [line.split(':')[0] for line in input_text.splitlines()]

# Join the usernames with commas
output_text = ",".join(usernames)

# Print the formatted usernames
print("Formatted Usernames:")
print(output_text)
