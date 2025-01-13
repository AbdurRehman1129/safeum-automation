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

clear_screen()
print_banner()
numbers = input("Enter the numbers separated by commas: ")

# Split the numbers by comma and process each one to remove '994' prefix
processed_numbers = [num[3:] if num.startswith('994') else num for num in numbers.split(',')]

# Join the processed numbers back into a single string
output = ",".join(processed_numbers)

# Print the result
print("Processed numbers:", output)
