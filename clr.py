import os

# SafeUM package name
PACKAGE_NAME = "com.safeum.android"

# Function to execute ADB commands
def adb_command(command):
    os.system(f"adb {command}")

# Check if device is connected
print("[*] Checking ADB connection...")
adb_command("devices")

# Clear SafeUM app data
print("[*] Clearing SafeUM app data...")
adb_command(f"shell pm clear {PACKAGE_NAME}")

# Grant all permissions
print("[*] Granting all permissions to SafeUM...")
adb_command(f"shell pm grant {PACKAGE_NAME} android.permission.READ_CONTACTS")
adb_command(f"shell pm grant {PACKAGE_NAME} android.permission.WRITE_CONTACTS")
adb_command(f"shell pm grant {PACKAGE_NAME} android.permission.READ_SMS")
adb_command(f"shell pm grant {PACKAGE_NAME} android.permission.SEND_SMS")
adb_command(f"shell pm grant {PACKAGE_NAME} android.permission.RECEIVE_SMS")
adb_command(f"shell pm grant {PACKAGE_NAME} android.permission.CALL_PHONE")
adb_command(f"shell pm grant {PACKAGE_NAME} android.permission.RECORD_AUDIO")
adb_command(f"shell pm grant {PACKAGE_NAME} android.permission.CAMERA")
adb_command(f"shell pm grant {PACKAGE_NAME} android.permission.ACCESS_FINE_LOCATION")
adb_command(f"shell pm grant {PACKAGE_NAME} android.permission.ACCESS_COARSE_LOCATION")

# Print completion message
print("[*] SafeUM data cleared and permissions granted successfully!")
