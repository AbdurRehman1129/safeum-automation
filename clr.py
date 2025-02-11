import os
def run_adb_command(command):
    return os.system(f"{command} >nul 2>&1")  # Redirect stdout to null, keep stderr

def open_safeum():
    command = f"adb shell am start -n com.safeum.android/im.sum.viewer.login.LoginActivity"
    result = run_adb_command(command)  # Use the helper function here
    if result == 0:
        print("SafeUM launched successfully.")
    else:
        print("Failed to launch SafeUM.")

def clear_safeum_data():
    command = f"adb shell pm clear com.safeum.android"
    run_adb_command(command)
    

def close_safeum():

    command = f"adb shell am force-stop com.safeum.android"
    run_adb_command(command)  # Use the helper function here


def enable_safeum_permissions():
    permissions = [
        "android.permission.CAMERA",
        "android.permission.RECORD_AUDIO",
        "android.permission.READ_EXTERNAL_STORAGE",
        "android.permission.WRITE_EXTERNAL_STORAGE",
        "android.permission.READ_CONTACTS",
        "android.permission.READ_PHONE_STATE"
    ]

    for permission in permissions:
        command = f"adb shell pm grant com.safeum.android {permission}"
        run_adb_command(command)

# Function to disable SafeUM app notifications
def disable_safeum_notifications():
    command = f"adb shell appops set com.safeum.android POST_NOTIFICATION deny"
    run_adb_command(command)
    
def close_and_open():
    close_safeum()
    clear_safeum_data()
    enable_safeum_permissions()
    disable_safeum_notifications()
    open_safeum()
 
close_and_open()
