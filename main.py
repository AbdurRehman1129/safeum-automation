import os
import time
import re
import json
import argparse

# Function to save the setup configuration
def save_setup(setup_name, setup_data):
    setups = load_setups()
    setups[setup_name] = setup_data
    with open("setups.json", "w", encoding="utf-8") as f:
        json.dump(setups, f, ensure_ascii=False, indent=4)
    print(f"Setup '{setup_name}' saved successfully!")

# Function to load all setups
def load_setups():
    if os.path.exists("setups.json"):
        with open("setups.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Function to setup the coordinates for UI elements
def setup_coordinates():
    print("Please enter the coordinates for the following UI elements:")

    # Collect the coordinates
    setup_data = {
        "username_field": input("Username field coordinates (x,y): ").strip(),
        "password_field": input("Password field coordinates (x,y): ").strip(),
        "login_button": input("Login button coordinates (x,y): ").strip(),
        "go_to_auth_button": input("GO TO AUTH button coordinates (x,y): ").strip(),
        "settings_button": input("Settings button coordinates (x,y): ").strip(),
        "account_control_button": input("Account control button coordinates (x,y): ").strip(),
        "logout_button": input("Logout button coordinates (x,y): ").strip(),
        "keep_in_device_button": input("Keep in device button coordinates (x,y): ").strip()
    }

    setup_name = input("Enter a name for this setup: ").strip()
    save_setup(setup_name, setup_data)

# Function to load a specific setup
def load_setup_by_name(setup_name):
    setups = load_setups()
    if setup_name in setups:
        return setups[setup_name]
    else:
        print(f"Setup '{setup_name}' not found!")
        return None

# Helper function to run ADB commands and suppress standard output while preserving errors
def run_adb_command(command):
    return os.system(f"{command} >nul 2>&1")  # Redirect stdout to null, keep stderr

# Function to check if the login page is visible
def is_login_page():
    run_adb_command("adb shell uiautomator dump /sdcard/window_dump.xml")
    run_adb_command("adb pull /sdcard/window_dump.xml .")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    return "com.safeum.android:id/et_login" in xml_content and "com.safeum.android:id/et_password" in xml_content and "com.safeum.android:id/login_button" in xml_content

# Function to check if the GO TO AUTH button is visible
def is_go_to_auth_button():
    run_adb_command("adb shell uiautomator dump /sdcard/window_dump.xml")
    run_adb_command("adb pull /sdcard/window_dump.xml .")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    return "GO TO AUTH" in xml_content

# Function to check if the progress bar is visible
def is_progress_bar_visible():
    run_adb_command("adb shell uiautomator dump /sdcard/window_dump.xml")
    run_adb_command("adb pull /sdcard/window_dump.xml .")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    return "android:id/progress" in xml_content

# Function to check if "Invite" or "Settings" button is visible
def check_for_buttons():
    run_adb_command("adb shell uiautomator dump /sdcard/window_dump.xml")
    run_adb_command("adb pull /sdcard/window_dump.xml .")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    if "Invite" in xml_content:
        return "invite"
    elif "Settings" in xml_content:
        return "settings"
    else:
        return None

# Function to automate login
def automate_login(username, password, setup_data):
    print(f"Logging in with username: {username}")
    username_coords = tuple(map(int, setup_data["username_field"].split(',')))
    password_coords = tuple(map(int, setup_data["password_field"].split(',')))
    login_coords = tuple(map(int, setup_data["login_button"].split(',')))

    run_adb_command(f"adb shell input tap {username_coords[0]} {username_coords[1]}")
    run_adb_command(f"adb shell input text {username}")
    run_adb_command(f"adb shell input tap {password_coords[0]} {password_coords[1]}")
    run_adb_command(f"adb shell input text {password}")
    run_adb_command(f"adb shell input tap {login_coords[0]} {login_coords[1]}")

# Launch SafeUM app
def launch_safeum():
    print("Launching SafeUM app...")
    run_adb_command("adb shell monkey -p com.safeum.android 1")

# Wait for progress bar to disappear
def wait_for_progress_bar_to_disappear():
    print("Waiting for the progress bar to disappear...")
    while True:
        if not is_progress_bar_visible():
            print("Progress bar disappeared!")
            break
        time.sleep(1)

# Click on the appropriate button
def click_button(button,setup_data):
    settings_coords = tuple(map(int, setup_data["settings_button"].split(',')))

    if button == "settings":
        print("Clicking the Settings button...")
        run_adb_command(f"adb shell input tap {settings_coords[0]} {settings_coords[1]}")

# Function to extract phone number from the screen XML
def extract_phone_number():
    print("Extracting phone number...")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    phone_number_pattern = r'\b9944[\d\s]{10}\b'
    phone_numbers = re.findall(phone_number_pattern, xml_content)
    if phone_numbers:
        for number in phone_numbers:
            print("Found phone number:", number)
        return phone_numbers
    else:
        return []

# Function to log out from SafeUM
def logout(setup_data,username):
    control_coords = tuple(map(int, setup_data["account_control_button"].split(',')))
    logout_coords = tuple(map(int, setup_data["logout_button"].split(',')))
    exit_coords = tuple(map(int, setup_data["keep_in_device_button"].split(',')))

    while True:
        run_adb_command("adb shell uiautomator dump /sdcard/window_dump.xml")
        run_adb_command("adb pull /sdcard/window_dump.xml .")
        with open("window_dump.xml", "r", encoding="utf-8") as file:
            xml_content = file.read()
        if "Account control" in xml_content:
            print("Found Account control, clicking button...")
            run_adb_command(f"adb shell input tap {control_coords[0]} {control_coords[1]}")
            break
        time.sleep(0.31)

    while True:
        run_adb_command("adb shell uiautomator dump /sdcard/window_dump.xml")
        run_adb_command("adb pull /sdcard/window_dump.xml .")
        with open("window_dump.xml", "r", encoding="utf-8") as file:
            xml_content = file.read()
        if username in xml_content:
            print("Username found, clicking logout...")
            run_adb_command(f"adb shell input tap {logout_coords[0]} {logout_coords[1]}")
            break
        time.sleep(0.31)

    while True:
        run_adb_command("adb shell uiautomator dump /sdcard/window_dump.xml")
        run_adb_command("adb pull /sdcard/window_dump.xml .")
        with open("window_dump.xml", "r", encoding="utf-8") as file:
            xml_content = file.read()
        if "Account exit" in xml_content:
            print("Found Account exit Page, clicking Keep on device...")
            run_adb_command(f"adb shell input tap {exit_coords[0]} {exit_coords[1]}")
            break
        time.sleep(0.1)
        
# Main function to login and logout multiple accounts
def main():
    parser = argparse.ArgumentParser(description="Automate SafeUM login process.")
    parser.add_argument("--setup", type=str, help="Specify the setup name to use.")
    args = parser.parse_args()

    # If a setup name is provided, load that setup
    setup_data = None
    if args.setup:
        setup_data = load_setup_by_name(args.setup)
        if setup_data:
            print(f"Loaded setup '{args.setup}' successfully.")
    
    if setup_data is None:
        # If no setup is provided or failed to load, ask the user to create a new one
        print("No setup provided or failed to load, please create a new one.")
        setup_coordinates()

    usernames = input("Enter usernames separated by commas: ").split(',')
    usernames = [username.strip() for username in usernames if username.strip()]
    password = input("Enter password for all accounts: ")
    auth_coords = tuple(map(int, setup_data["go_to_auth_button"].split(',')))
    # Load existing data from extracted_phone_numbers.json if it exists
    extracted_data = {}
    if os.path.exists("extracted_phone_numbers.json"):
        with open("extracted_phone_numbers.json", "r", encoding="utf-8") as json_file:
            extracted_data = json.load(json_file)

    # Launch SafeUM app
    launch_safeum()
    time.sleep(3)  # Wait for the app to load
    count_usernames(usernames)
    for index,username in enumerate(usernames,start=1):
        # Skip the username if it already has a phone number in the extracted data
        if username in extracted_data:
            print(f"{index}. Skipping {username} as it already has extracted phone numbers.")
            continue

        print(f"\n{index}. Processing account: {username}")

        # Login or handle GO TO AUTH
        for attempt in range(10):
            print(f"Checking for login page or GO TO AUTH button... Attempt {attempt + 1}")
            if is_go_to_auth_button():
                print("GO TO AUTH button found! Clicking it...")
                run_adb_command(f"adb shell input tap {auth_coords[0]} {auth_coords[1]}")       
                time.sleep(0.21)  # Wait for the transition
            if is_login_page():
                print("Login page found!")
                automate_login(username, password,setup_data)
                break
            else:
                print("Neither GO TO AUTH nor Login page found.")
            time.sleep(2)
        else:
            print(f"Login page not found for {username}, skipping...")
            continue

        # Wait for progress bar
        wait_for_progress_bar_to_disappear()
        print("Checking for Settings button...")
        while True:
            button = check_for_buttons()

            if button == "invite":
                click_button("settings",setup_data)
                break
            elif button == "settings":
                click_button("settings",setup_data)
                break

        time.sleep(0.12)
        phone_numbers = extract_phone_number()
        if phone_numbers:
            extracted_data[username] = phone_numbers
            # Append new data to the JSON file without overwriting
            with open("extracted_phone_numbers.json", "w", encoding="utf-8") as json_file:
                json.dump(extracted_data, json_file, ensure_ascii=False, indent=4)
            print(f"Phone number for {username} has been saved to 'extracted_phone_numbers.json'.")

        # Logout
        logout(setup_data,username)
        print(f"Logged out from account: {username}\n")
        clear_screen()
def count_usernames(usernames):
    
    print(f'Total usernames are: {len(usernames)}')

def display_accounts(file_path):
    # Open and load the JSON data
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Display the accounts in a readable format
    index=1
    for username, numbers in data.items():
        
        for number in numbers:
            print(f"{index}. {username} : {number}")
            index+=1

def clear_screen():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Linux/Unix/MacOS
    else:
        os.system('clear')

def displaymenu():
    clear_screen()
    print("\nMENU:")
    print("1. Extract phone numbers from SafeUM.")
    print("2. Display Extracted accounts.")
    print("3. Setup coordinates.")
    print("4. Display Numbers.")
    print("5. Exit")

def display_phone_numbers():
    # Load the JSON data
    with open('extracted_phone_numbers.json', 'r') as file:
        data = json.load(file)
    
    # Extract and format the phone numbers
    phone_numbers = []
    for key, value in data.items():
        for number in value:
            # Remove spaces and append to the list
            formatted_number = number.replace(' ', '')
            phone_numbers.append(formatted_number)
    
    # Print the numbers, separated by commas
    print(', '.join(phone_numbers))

if __name__ == "__main__":
    
    while(True):
        displaymenu()
        choice =int(input("\nEnter Your choice: "))
        if choice == 1:
            main()
            input("\nPress any key to go back to main menu...")
        elif choice == 2:
            display_accounts('extracted_phone_numbers.json')
            input("\nPress any key to go back to main menu...")
        elif choice == 3:
            setup_coordinates()
            input("\nPress any key to go back to main menu...")
        elif choice == 4:
            display_phone_numbers()
            input("\nPress any key to go back to main menu...")
        elif choice == 5:
            exit("Exiting...")
        else:
            print("Invalid input...")
            input("\nPress any key to go back to main menu...")
