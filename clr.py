import os

# Correct package name for SafeUM
PACKAGE_NAME = "com.safeum.android"

# Function to run ADB commands quietly
def adb_command(command):
    return os.popen(f"adb {command} 2>/dev/null").read().strip()

# Check ADB connection
print("[*] Checking ADB connection...")
adb_command("devices")

# Clear SafeUM app data
print("[*] Clearing SafeUM app data...")
adb_command(f"shell pm clear {PACKAGE_NAME}")

# Get only permissions requested by the app
print("[*] Checking required permissions...")
requested_permissions = adb_command(f"shell dumpsys package {PACKAGE_NAME} | grep permission").split("\n")
permissions = [perm.split(":")[0].strip() for perm in requested_permissions if "granted=false" in perm]

# Grant only requested permissions
if permissions:
    print("[*] Granting necessary permissions...")
    for perm in permissions:
        adb_command(f"shell pm grant {PACKAGE_NAME} {perm}")

print("[*] SafeUM data cleared and permissions granted successfully!")
