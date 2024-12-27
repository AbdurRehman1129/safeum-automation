import re
import pyfiglet
from colorama import Fore, Style, init
import os
import platform
import shutil

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def print_banner():
    banner = pyfiglet.Figlet(font="small")
    banner_text = banner.renderText("DARK DEVIL")
    terminal_width = shutil.get_terminal_size().columns
    banner_lines = banner_text.split('\n')
    
    # Center each line of the banner
    centered_banner = []
    for line in banner_lines:
        centered_line = line.center(terminal_width)
        centered_banner.append(centered_line)

    # Print the centered banner
    print(Fore.CYAN + '\n'.join(centered_banner))

    # Center and style the Author/Github line with separate colors
    author_line = "Author/Github: "
    github_handle = "@AbdurRehman1129"
    author_line_colored = Fore.YELLOW + author_line + Fore.GREEN + github_handle + Style.RESET_ALL
    print(author_line_colored.center(terminal_width) + "\n")

def extract_and_format_phone_numbers(text):
    # Define a regex pattern to match phone numbers starting with 9944, allowing spaces in between digits
    pattern = r"9944[ \d]{8,}"  # Matches '9944' followed by 10 or more spaces/digits
    
    # Find all matching phone numbers
    matches = re.findall(pattern, text)
    
    # Clean phone numbers: Remove spaces and '+' if present
    cleaned_numbers = [re.sub(r"[ +]", "", match) for match in matches]
    
    return cleaned_numbers

def format_numbers_in_groups(numbers, group_size):
    # Divide the numbers into groups of `group_size`
    grouped_numbers = [numbers[i:i + group_size] for i in range(0, len(numbers), group_size)]
    
    # Convert groups into string format
    formatted_output = "\n\n".join([",".join(group) for group in grouped_numbers])
    return formatted_output

while True:
    clear_screen()
    print_banner()
    
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
    cleaned_numbers = extract_and_format_phone_numbers(text)

    if cleaned_numbers:
        # Ask the user for the group size
        while True:
            try:
                group_size = int(input("Enter the number of phone numbers per group: "))
                if group_size <= 0:
                    print(Fore.RED + "Group size must be a positive integer. Try again." + Style.RESET_ALL)
                    continue
                break
            except ValueError:
                print(Fore.RED + "Invalid input. Please enter a valid integer." + Style.RESET_ALL)

        # Output the formatted result
        formatted_output = format_numbers_in_groups(cleaned_numbers, group_size)
        print(Fore.GREEN + "Formatted Phone Numbers in Groups:\n" + Style.RESET_ALL)
        print(formatted_output)
    else:
        print(Fore.RED + "No valid phone numbers found in the text." + Style.RESET_ALL)
    
    # Ask the user if they want to format more numbers
    while True:
        choice = input("\nFormat more numbers (Y/N): ").lower()
        if choice == 'y':
            break
        elif choice == 'n':
            exit()
        else:
            print(Fore.RED + "Invalid Input. Try again...." + Style.RESET_ALL)
