import os
import time
import re
import json
import argparse
import sys

def update_script():
    os.system("git pull")
    input("\nPress any key to apply changings now....")
    os.execv(sys.executable, ['python'] + sys.argv)  # Restart script

def save_setup(setup_name, setup_data):
    setups = load_setups()
    setups[setup_name] = setup_data
    with open("setups.json", "w", encoding="utf-8") as f:
        json.dump(setups, f, ensure_ascii=False, indent=4)
    print(f"Setup '{setup_name}' saved successfully!")

def load_setups():
    if os.path.exists("setups.json"):
        with open("setups.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def setup_coordinates():
    print("Please enter the coordinates for the following UI elements:")

    # Collect the coordinates
    setup_data = {
        "username_field": input("Username field coordinates (x,y): ").strip(),
        "password_field": input("Password field coordinates (x,y): ").strip(),
        "login_button": input("Login button coordinates (x,y): ").strip(),
        "settings_button": input("Settings button coordinates (x,y): ").strip(),
        "close_app": input("Close app button coordinates (x,y): ").strip(),
    }

    setup_name = input("Enter a name for this setup: ").strip()
    save_setup(setup_name, setup_data)

def update_coordinates(setup_data):
    setups = load_setups()
    if not setups:
        print("No setups found.")
        return

    print("Available setups:")
    for i, name in enumerate(setups.keys(), start=1):
        print(f"{i}. {name}")

    while True:
        choice = input("Enter the number of the setup you want to update: ").strip()
        try:
            choice = int(choice)
            if 1 <= choice <= len(setups):
                setup_name = list(setups.keys())[choice - 1]
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    setup_data = setups[setup_name]
    while True:
        print("\nCurrent coordinates:")
        for i, (key, value) in enumerate(setup_data.items(), start=1):
            print(f"{i}. {key}: {value}")

        choice = input("\nEnter the number of the coordinate you want to change (or 'b' to go back to main menu): ").strip()
        if choice.lower() == 'b':
            break

        try:
            choice = int(choice)
            if 1 <= choice <= len(setup_data):
                key_to_update = list(setup_data.keys())[choice - 1]
                new_value = input(f"Enter new coordinates for {key_to_update} (x,y): ").strip()
                setup_data[key_to_update] = new_value
                save_setup(setup_name, setup_data)
                print(f"Updated {key_to_update} to {new_value}")
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def load_setup_by_name(setup_name):
    setups = load_setups()
    if setup_name in setups:
        return setups[setup_name]
    else:
        print(f"Setup '{setup_name}' not found!")
        return None

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
       
        elif element == "stopped" and ("stop" in xml_content or "android:id/alertTitle" in xml_content):
            return True
        
        elif element == "progress_bar" and "android:id/progress" in xml_content:
            return True

        elif element == "error" and "Security params error. Try Again" in xml_content:
            return True

        elif element == "invite" and "Invite" in xml_content:
            return True

        elif element == "settings" and "Settings" in xml_content:
            return True
        
        elif element == "safeum" and ("ENTER YOUR DETAILS" in xml_content):
            return True
        
        elif element == "message" and ("Enter your message here" in xml_content and "com.safeum.android:id/editMessages" in xml_content):
            return True

def load_usernames_from_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().strip()  # Read entire file and remove trailing spaces

        # Check if the file contains comma-separated usernames
        if ',' in content:
            usernames = [username.strip() for username in content.split(',') if username.strip()]
        else:
            usernames = [line.strip() for line in content.splitlines() if line.strip()]
        print(f"Usernames loaded from File {file_path} : {len(usernames)} ")
        return usernames
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        exit(1)

def initialize_setup():
    parser = argparse.ArgumentParser(description="Automate SafeUM login process.")
    parser.add_argument("--setup", type=str, help="Specify the setup name to use.")
    parser.add_argument("--file", type=str, help="Specify a file containing usernames.")

    args = parser.parse_args()

    # If a setup name is provided, load that setup
    setup_data = None
    file_path = args.file
    if args.setup:
        setup_data = load_setup_by_name(args.setup)
        if setup_data:
            print(f"Loaded setup '{args.setup}' successfully.")
    if setup_data is None:
        # If no setup is provided or failed to load, check for existing setups
        existing_setups = load_setups()
        if existing_setups:
            print("No setup name provided.")
            choice = input("Do you want to choose an existing setup or create a new one? (E/C): ").strip().lower()
            if choice == 'e':
                print("Available setups:")
                for i, name in enumerate(existing_setups.keys(), start=1):
                    print(f"{i}. {name}")
                while True:
                    setup_choice = input("Enter the number of the setup you want to use: ").strip()
                    try:
                        setup_choice = int(setup_choice)
                        if 1 <= setup_choice <= len(existing_setups):
                            setup_name = list(existing_setups.keys())[setup_choice - 1]
                            setup_data = existing_setups[setup_name]
                            print(f"Loaded setup '{setup_name}' successfully.")
                            break
                        else:
                            print("Invalid choice. Please try again.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")
            else:
                print("Please create a new setup.")
                setup_coordinates()
        else:
            print("No setups found. Please create a new one.")
            setup_coordinates()
    # Verify that all required coordinates are available in setup_data
    required_coordinates = [
        "username_field", "password_field", "login_button",
        "settings_button", "close_app"
    ]
    
    missing_coordinates = [coord for coord in required_coordinates if coord not in setup_data or not setup_data[coord]]
    
    if missing_coordinates:
        print("The following coordinates are missing or empty in the setup data:")
        for coord in missing_coordinates:
            setup_data[coord] = input(f"Please enter the coordinates for {coord} (x,y): ").strip()
        save_setup(args.setup, setup_data)
        print("Missing coordinates have been added and saved.")
    return setup_data ,file_path

def click_button(button,setup_data,device_id):
    username_coords = tuple(map(int, setup_data["username_field"].split(',')))
    password_coords = tuple(map(int, setup_data["password_field"].split(',')))
    login_coords = tuple(map(int, setup_data["login_button"].split(',')))
    settings_coords = tuple(map(int, setup_data["settings_button"].split(',')))
    close_coords = tuple(map(int, setup_data["close_app"].split(',')))

    if button == "username":
        run_adb_command(f"adb -s {device_id} shell input tap {username_coords[0]} {username_coords[1]}")
    elif button == "password":
        run_adb_command(f"adb -s {device_id} shell input tap {password_coords[0]} {password_coords[1]}")
    elif button == "login":
        run_adb_command(f"adb -s {device_id} shell input tap {login_coords[0]} {login_coords[1]}")
    elif button == "settings":
        print("Clicking the settings button...")
        run_adb_command(f"adb -s {device_id} shell input tap {settings_coords[0]} {settings_coords[1]}")
    elif button == "close_app":
        print("Clicking the close button...")
        run_adb_command(f"adb -s {device_id} shell input tap {close_coords[0]} {close_coords[1]}")
    
def automate_login(username, password, setup_data,device_id,index,total):
    clear_screen()
    print(f"{index}/{total}. Logging in with username: {username}")
    click_button('username',setup_data,device_id)
    time.sleep(0.5)
    run_adb_command(f"adb -s {device_id} shell input text {username}")
    print("Username Entered.")
    time.sleep(0.5)
    click_button('password',setup_data,device_id)
    time.sleep(0.5)
    run_adb_command(f"adb -s {device_id} shell input text {password}")
    print("Password Entered.")
    time.sleep(0.5)
    while True:
        click_button('login',setup_data,device_id)
        print("Check Button Clicked.")
        found_progress = check_for(device_id, 'progress_bar')
        if found_progress:
            break

def wait_for_progress_bar_to_disappear(device_id,setup_data):
    print("Waiting for the progress bar to disappear...")
    start_time = time.time()
    while True:
        found_progress = check_for(device_id, 'progress_bar')
        if not found_progress:
            print("\r" + " " * len("Waiting for the progress bar to disappear..."), end='', flush=True)
            print("\rProgress bar disappeared!")
            break
        elif time.time() - start_time > 300:  
            print("\r" + " " * len("Waiting for the progress bar to disappear..."), end='', flush=True)
            print("\rTimeout 5 minutes. Starting process again...")
            click_button('settings',setup_data,device_id)
            break
        
def extract_phone_number(device_id,setup_data):
    print("Extracting phone number...")
    while True:
        run_adb_command(f"adb -s {device_id} shell uiautomator dump /sdcard/window_dump.xml")
        run_adb_command(f"adb -s {device_id} pull /sdcard/window_dump.xml .")
        with open("window_dump.xml", "r", encoding="utf-8") as file:
            xml_content = file.read()
        phone_number_pattern_994 = r'\b9944[\d\s]{10}\b'
        phone_number_pattern_371 = r'\b3712[\d\s]{9}\b' 
        phone_numbers_994 = re.findall(phone_number_pattern_994, xml_content)
        phone_numbers_371 = re.findall(phone_number_pattern_371, xml_content)

        phone_numbers = phone_numbers_994 + phone_numbers_371
        
        if phone_numbers:
            phone_numbers = [number.replace(" ", "") for number in phone_numbers]  # Normalize the phone number format
            print(f"Phone number found: {phone_numbers}")
            return phone_numbers
        elif check_for(device_id, 'message'):
            phone_number_pattern_994 = r'\b9944\d{8}\b'
            phone_numbers_994 = re.findall(phone_number_pattern_994, xml_content)
            if phone_numbers_994:
                return phone_numbers_994
            else:
                run_adb_command(f"adb -s {device_id} shell input keyevent 4")  # Back button
                time.sleep(0.5)
                click_button('settings',setup_data,device_id)
                extract_phone_number(device_id,setup_data)
        
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
    extracted_data = load_extracted_data()
    
    for number in phone_numbers:
        if number.startswith("9944"):
            extracted_data = {username: phone_numbers, **extracted_data}
        elif number.startswith("3712"):
            extracted_data[username] = phone_numbers
    
    with open("extracted_phone_numbers.json", "w", encoding="utf-8") as json_file:
        json.dump(extracted_data, json_file, ensure_ascii=False, indent=4)
        
    print(f"Phone number for {username} has been saved to 'extracted_phone_numbers.json'.")

def clear_safeum_data(device_id):
    command = f"adb -s {device_id} shell pm clear com.safeum.android"
    run_adb_command(command)
    
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

def disable_safeum_notifications(device_id):
    command = f"adb -s {device_id} shell appops set com.safeum.android POST_NOTIFICATION deny"
    run_adb_command(command)
    
def close_and_open(device_id,setup_data):
    close_safeum(device_id)
    clear_safeum_data(device_id)
    enable_safeum_permissions(device_id)
    disable_safeum_notifications(device_id)
    open_safeum(device_id)
    click_button('username',setup_data,device_id)
    time.sleep(2)
    found_login = check_for(device_id, "login_page")
    if found_login:
        return 
    elif not check_for(device_id,'safeum'):
        if check_for(device_id,'stopped'):
            click_button('close_app',setup_data,device_id)
            click_button('settings',setup_data,device_id)
        close_and_open(device_id,setup_data)

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

def check_for_error_or_settings(setup_data,device_id,username):
    while True:  
        found_settings = check_for(device_id,"settings")
        if found_settings:
            click_button('settings',setup_data,device_id)
            if not username:
                continue
            else:
                return True
        
        else:    
            found_login = check_for(device_id, 'login_page')
        if found_login:
            print("Login page found again. Restarting the process for this username...")
            return False
        else:   
            found_stop = check_for(device_id, 'stopped')
        if found_stop:
            print("SafeUM is stopped...")
            click_button('close_app',setup_data,device_id)
            return False
        
        else:
            found_error = check_for(device_id, 'error')
        if found_error:
            print("Error found. Closing and reopening the app...")
            return False 
        
def automate_safeum(username, password, setup_data, selected_device,index,total):
    close_and_open(selected_device,setup_data)
    automate_login(username, password, setup_data,selected_device, index,total)
    wait_for_progress_bar_to_disappear(selected_device,setup_data)
    if not check_for_error_or_settings(setup_data,selected_device,username):
        # If an error was found, retry the login process
        print("Retrying login process...")
        automate_safeum(username, password, setup_data, selected_device,index,total)
        return
    phone_numbers = extract_phone_number(selected_device,setup_data)
    if phone_numbers:
        save_phone_number(username, phone_numbers)
        
    clear_screen()
    return

def main():
    
    setup_data,file_path = initialize_setup()
    selected_device = ask_to_select_device()
    clear_screen()
    extracted_data = load_extracted_data()
    if file_path:
        usernames = load_usernames_from_file(file_path)
        password = input("Enter password for all accounts: ")

    else:    
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

    print(f"Total numbers are {index-1}")

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
    print("4. Update coordinates.")
    print("5. Display Numbers.")
    print("6. Handle Duplicate Numbers.")
    print("7. Update Script.")
    print("8. Exit")

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
    close_and_open(selected_device,setup_data)
    automate_login(username, password, setup_data,selected_device, index,total)
    wait_for_progress_bar_to_disappear(selected_device,setup_data)
    if not check_for_error_or_settings(setup_data,selected_device,username):
        # If an error was found, retry the login process
        print("Retrying login process...")
        handle_duplicated_numbers(username, password, setup_data, selected_device,index,total)
        return
    phone_numbers = extract_phone_number(selected_device,setup_data)
    if phone_numbers:
        save_phone_number(username, phone_numbers)
        
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
            setup_data = initialize_setup()
            update_coordinates(setup_data)
        elif choice == 5:
            display_phone_numbers()
            input("\nPress any key to go back to main menu...")
        elif choice == 6:
            handle_duplicates("extracted_phone_numbers.json")
            input("\nPress any key to go back to main menu...")
        elif choice == 7:  
            update_script()
        elif choice == 8:
            exit("Exiting...")
        else:
            print("Invalid input...")
            input("\nPress any key to go back to main menu...")
