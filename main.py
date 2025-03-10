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

def get_connected_devices():
    devices_output = os.popen("adb devices").read()
    devices = []
    if devices_output:
        for line in devices_output.split("\n")[1:]:
            if line.strip():
                parts = line.split("\t")
                if len(parts) == 2 and parts[1] == "device":
                    devices.append(parts[0])
    return devices

def ask_to_select_device():
    devices = get_connected_devices()
    if not devices:
        print("No devices connected.")
        
    elif len(devices) == 1:
        selected_device = devices[0]
        return selected_device
    else:
        print("Connected devices:")
        for i, device in enumerate(devices):
            print(f"{i + 1}. {device}")
        choice = input("Select a device (1, 2, ...): ").strip()
        try:
            selected_device = devices[int(choice) - 1]
            return selected_device
        except (IndexError, ValueError):
            print("Invalid choice. Exiting.")

def open_safeum(device_id):
    command = f"adb -s {device_id} shell am start -n com.safeum.android/im.sum.viewer.login.LoginActivity"
    result = run_adb_command(command)  # Use the helper function here
    if result == 0:
        print("SafeUM launched successfully.")
    else:
        print("Failed to launch SafeUM.")

def close_safeum(device_id):

    command = f"adb -s {device_id} shell am force-stop com.safeum.android"
    run_adb_command(command)  # Use the helper function here

def check_for(device_id, element):
    
        run_adb_command(f"adb -s {device_id} shell uiautomator dump /sdcard/window_dump.xml")
        run_adb_command(f"adb -s {device_id} pull /sdcard/window_dump.xml .")

        with open("window_dump.xml", "r", encoding="utf-8") as file:
            xml_content = file.read()

        if element == "login_page" and (
            "com.safeum.android:id/et_login" in xml_content and
            "com.safeum.android:id/et_password" in xml_content and
            "com.safeum.android:id/login_button" in xml_content
        ):
            return True  
            
        elif element == "auth_button" and "GO TO AUTH" in xml_content:
            return True

        elif element == "progress_bar" and "android:id/progress" in xml_content:
            return True

        elif element == "error" and "Security params error. Try Again" in xml_content:
            return True

        elif element == "invite" and "Invite" in xml_content:
            return True

        elif element == "settings" and "Settings" in xml_content:
            return True
        
        elif element == "stopped" and "SafeUM has stopped." in xml_content or "SafeUM keeps stopping." in xml_content:
            return True

def initialize_setup():
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
        # If no setup is provided or failed to load, check for existing setups
        existing_setups = load_setups()
        if existing_setups:
            print("No setup provided or failed to load. Available setups:")
            for setup_name in existing_setups.keys():
                print(f"- {setup_name}")
            choice = input("Would you like to select one of these setups? (yes/no): ").strip().lower()
            if choice == 'yes':
                selected_setup = input("Enter the name of the setup you want to use: ").strip()
                setup_data = load_setup_by_name(selected_setup)
                if setup_data:
                    print(f"Loaded setup '{selected_setup}' successfully.")
                else:
                    print(f"Setup '{selected_setup}' not found. Please create a new one.")
                    setup_coordinates()
            else:
                print("Please create a new setup.")
                setup_coordinates()
        else:
            print("No setups found. Please create a new one.")
            setup_coordinates()
    
    return setup_data

def click_button(button,setup_data,device_id):
    username_coords = tuple(map(int, setup_data["username_field"].split(',')))
    password_coords = tuple(map(int, setup_data["password_field"].split(',')))
    login_coords = tuple(map(int, setup_data["login_button"].split(',')))
    control_coords = tuple(map(int, setup_data["account_control_button"].split(',')))
    logout_coords = tuple(map(int, setup_data["logout_button"].split(',')))
    exit_coords = tuple(map(int, setup_data["keep_in_device_button"].split(',')))
    auth_coords = tuple(map(int, setup_data["go_to_auth_button"].split(',')))
    settings_coords = tuple(map(int, setup_data["settings_button"].split(',')))

    if button == "username":
        run_adb_command(f"adb -s {device_id} shell input tap {username_coords[0]} {username_coords[1]}")
    elif button == "password":
        run_adb_command(f"adb -s {device_id} shell input tap {password_coords[0]} {password_coords[1]}")
    elif button == "login":
        run_adb_command(f"adb -s {device_id} shell input tap {login_coords[0]} {login_coords[1]}")
    elif button == "auth":
        print("Clicking GO TO AUTH button...")
        run_adb_command(f"adb -s {device_id} shell input tap {auth_coords[0]} {auth_coords[1]}")
    elif button == "settings":
        print("Clicking the settings button...")
        run_adb_command(f"adb -s {device_id} shell input tap {settings_coords[0]} {settings_coords[1]}")
    elif button == "control":
        print("Clicking the Account control button...")
        run_adb_command(f"adb -s {device_id} shell input tap {control_coords[0]} {control_coords[1]}")
    elif button == "logout":
        print("Clicking the logout button...")
        run_adb_command(f"adb -s {device_id} shell input tap {logout_coords[0]} {logout_coords[1]}")
    elif button == "exit":
        print("Clicking the exit button...")
        run_adb_command(f"adb -s {device_id} shell input tap {exit_coords[0]} {exit_coords[1]}")
    
def automate_login(username, password, setup_data,device_id,index,total):
    clear_screen()
    print(f"{index}/{total}. Logging in with username: {username}")
    click_button('username',setup_data,device_id)
    run_adb_command(f"adb -s {device_id} shell input text {username}")
    click_button('password',setup_data,device_id)
    run_adb_command(f"adb -s {device_id} shell input text {password}")
    click_button('login',setup_data,device_id)

# Wait for progress bar to disappear
def wait_for_progress_bar_to_disappear(device_id,setup_data):
    print("Waiting for the progress bar to disappear...")
    start_time = time.time()
    while True:
        found_progress = check_for(device_id, 'progress_bar')
        if not found_progress:
            print("\r" + " " * len("Waiting for the progress bar to disappear..."), end='', flush=True)
            print("\rProgress bar disappeared!")
            break
        elif time.time() - start_time > 600:  # 10 minutes = 600 seconds
            print("\r" + " " * len("Waiting for the progress bar to disappear..."), end='', flush=True)
            print("\rTimeout 10 minutes. Starting process again...")
            click_button('logout',setup_data,device_id)
            break
        
# Function to extract phone number from the screen XML
def extract_phone_number(device_id):
    print("Extracting phone number...")
    while True:
        run_adb_command(f"adb -s {device_id} shell uiautomator dump /sdcard/window_dump.xml")
        run_adb_command(f"adb -s {device_id} pull /sdcard/window_dump.xml .")
        with open("window_dump.xml", "r", encoding="utf-8") as file:
            xml_content = file.read()
        phone_number_pattern_994 = r'\b9944[\d\s]{10}\b'
        phone_number_pattern_371 = r'\b3712[\d\s]{9}\b' 
        phone_numbers = re.findall(phone_number_pattern_994, xml_content)
        phone_numbers = re.findall(phone_number_pattern_371, xml_content)
        
        if phone_numbers:
            phone_numbers = [number.replace(" ", "") for number in phone_numbers]  # Normalize the phone number format
            print(f"Phone number found: {phone_numbers}")
            return phone_numbers
        
def load_extracted_data():
    """Load existing data from extracted_phone_numbers.json if it exists."""
    extracted_data = {}
    if os.path.exists("extracted_phone_numbers.json"):
        with open("extracted_phone_numbers.json", "r", encoding="utf-8") as json_file:
            extracted_data = json.load(json_file)
    return extracted_data

def is_username_present(username, extracted_data):
    """Check if the username is already present in the extracted data."""
    return username in extracted_data

def save_phone_number(username, phone_numbers):
    """Save the phone number along with its username in the JSON file."""
    extracted_data = load_extracted_data()
    extracted_data[username] = phone_numbers
    with open("extracted_phone_numbers.json", "w", encoding="utf-8") as json_file:
        json.dump(extracted_data, json_file, ensure_ascii=False, indent=4)
    print(f"Phone number for {username} has been saved to 'extracted_phone_numbers.json'.")

# Function to clear all data of the SafeUM app
def clear_safeum_data(device_id):
    command = f"adb -s {device_id} shell pm clear com.safeum.android"
    run_adb_command(command)
    
# Function to enable all required permissions for the SafeUM app
def enable_safeum_permissions(device_id):
    permissions = [
        "android.permission.CAMERA",
        "android.permission.RECORD_AUDIO",
        "android.permission.READ_EXTERNAL_STORAGE",
        "android.permission.WRITE_EXTERNAL_STORAGE",
        "android.permission.READ_CONTACTS",
        "android.permission.READ_PHONE_STATE"
    ]

    for permission in permissions:
        command = f"adb -s {device_id} shell pm grant com.safeum.android {permission}"
        run_adb_command(command)

# Function to disable SafeUM app notifications
def disable_safeum_notifications(device_id):
    command = f"adb -s {device_id} shell appops set com.safeum.android POST_NOTIFICATION deny"
    run_adb_command(command)
    
def close_and_open(device_id):
    close_safeum(device_id)
    clear_safeum_data(device_id)
    enable_safeum_permissions(device_id)
    disable_safeum_notifications(device_id)
    open_safeum(device_id)
 
def retry_check_for(setup_data, device_id):
    found_login = False
    found_auth = False
    while True:
        for attempt in range(10):
            found_login = check_for(device_id, "login_page")
            
            if found_login: 
                break
            found_auth = check_for(device_id, "auth_button")
            if found_auth:
                click_button('auth', setup_data, device_id)
                break
        if found_auth or found_login:
            break
        open_safeum(device_id)  # Retry by  reopening the device

def check_for_error_or_settings(setup_data,device_id):
    while True:  # Infinite loop until we find either an error or settings
        found_error = check_for(device_id, 'error')
        found_settings = check_for(device_id,"settings")
        found_login = check_for(device_id, 'login_page')
        if found_settings:
            click_button('settings',setup_data,device_id)
            return True
        
        elif found_error:
            print("Error found. Closing and reopening the app...")
            return False 

        elif found_login:
            print("Login page found again. Restarting the process for this username...")
            return False

def check_for_logout_things(username,device_id,element):
    while True:
        run_adb_command(f"adb -s {device_id} shell uiautomator dump /sdcard/window_dump.xml")
        run_adb_command(f"adb -s {device_id} pull /sdcard/window_dump.xml .")

        with open("window_dump.xml", "r", encoding="utf-8") as file:
            xml_content = file.read()
        if element == 'account_control' and "Account control" in xml_content:
            return True
        elif element == 'logout_button' and username in xml_content:
            return True
        elif element == 'exit' and "Account exit" in xml_content:
            return True

def logout_safeum(username,setup_data,device_id):
    while True:
        if check_for_logout_things(username,device_id,'account_control'):
            click_button('control',setup_data,device_id)
            break
    while True:
        if check_for_logout_things(username,device_id,'logout_button'):
            click_button('logout',setup_data,device_id)
            break
    while True:   
        if check_for_logout_things(username,device_id,'exit'):
            click_button('exit',setup_data,device_id)
            break
    while not check_for(device_id, 'login_page'):
        time.sleep(1)
    return

def automate_safeum(username, password, setup_data, selected_device,index,total):
    close_and_open(selected_device)
    if check_for(selected_device,'stopped'):
        click_button('logout',setup_data,selected_device)
    retry_check_for(setup_data,selected_device)
    automate_login(username, password, setup_data,selected_device, index,total)
    wait_for_progress_bar_to_disappear(selected_device,setup_data)
    if not check_for_error_or_settings(setup_data,selected_device):
        # If an error was found, retry the login process
        print("Retrying login process...")
        automate_safeum(username, password, setup_data, selected_device,index,total)
        return
    phone_numbers = extract_phone_number(selected_device)
    if phone_numbers:
        save_phone_number(username, phone_numbers)
    logout_safeum(username,setup_data,selected_device)
    clear_screen()
    return

def main():
    
    setup_data = initialize_setup()
    selected_device = ask_to_select_device()
    clear_screen()
    extracted_data = load_extracted_data()

    usernames = input("Enter usernames separated by commas: ").split(',')
    usernames = [username.strip() for username in usernames if username.strip()]
    password = input("Enter password for all accounts: ")
    total = len(usernames)
    for index,username in enumerate(usernames,start=1):
        if is_username_present(username, extracted_data):
            print(f"{index}/{total}. Skipping {username} as it already has extracted phone numbers.")
            continue  
        else:
            automate_safeum(username, password, setup_data, selected_device,index,total)

def display_accounts(file_path):
    # Open and load the JSON data
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Display the accounts in a readable format
    index=1
    for username, numbers in data.items():
        
        for number in numbers:
            number = number.replace(" ", "")  # Normalize the phone number format
            print(f"Number: {number} , Username: {username}")
            index+=1

    print(f"Total numbers are {index}")

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
    print("5. Handle Duplicate Numbers.")
    print("6. Exit")

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
    print(','.join(phone_numbers))

def handle_duplicated_numbers(username, password, setup_data, selected_device,index,total):
    close_and_open(selected_device)
    retry_check_for(setup_data,selected_device)
    automate_login(username, password, setup_data,selected_device,index,total)
    wait_for_progress_bar_to_disappear(selected_device,setup_data)
    time.sleep(1)
    if not check_for_error_or_settings(setup_data,selected_device):
        # If an error was found, retry the login process
        print("Retrying login process...")
        handle_duplicated_numbers(username, password, setup_data, selected_device,index,total)
        return
    new_phone_numbers = extract_phone_number(selected_device)
    if new_phone_numbers:
        save_phone_number(username, new_phone_numbers)
    logout_safeum(username,setup_data,selected_device)
    clear_screen()
    return
    
def find_duplicates(file_path):

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    phone_to_users = {}
    for username, numbers in data.items():
        for number in numbers:
            number = number.replace(" ", "")  # Normalize the phone number format
            if number in phone_to_users:
                phone_to_users[number].append(username)
            else:
                phone_to_users[number] = [username]

    duplicates = {phone: users for phone, users in phone_to_users.items() if len(users) > 1}
    return duplicates

def handle_duplicates(file_path):

    duplicates = find_duplicates(file_path)
    total = len(duplicates)
    if not duplicates:
        print("No duplicate phone numbers found.")
        return

    print("Found duplicate phone numbers:")
    for phone, users in duplicates.items():
        print(f"Phone: {phone}, Usernames: {users}")

    setup_data = initialize_setup()
    selected_device = ask_to_select_device()
    password = input("Enter password for all accounts: ")
    clear_screen()
    open_safeum(selected_device)
    time.sleep(3)
    for phone, usernames in duplicates.items():
        for index,username in enumerate(usernames,start=1):
            handle_duplicated_numbers(username, password, setup_data, selected_device,index,total)

    print("Duplicate handling completed!")

# Add this option to your menu
if __name__ == "__main__":
    while True:
        displaymenu()
        choice = int(input("\nEnter your choice: "))
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
            handle_duplicates("extracted_phone_numbers.json")
            input("\nPress any key to go back to main menu...")
        elif choice == 6:
            exit("Exiting...")
        else:
            print("Invalid input...")
            input("\nPress any key to go back to main menu...")
