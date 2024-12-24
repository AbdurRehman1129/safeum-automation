### SafeUM Automation Script: A Powerful ADB-Based Automation Tool for Account Management

This repository provides a script to automate the login, phone number extraction, and logout processes in the SafeUM Android application. It uses **ADB (Android Debug Bridge)** to interact with the app, perform UI actions, and handle multiple accounts with ease.

---

#### **Features**
- Automates the SafeUM login process for multiple accounts.
- Extracts phone numbers directly from the app's screen.
- Configurable setup for UI element coordinates, saved for future reuse.
- Handles UI transitions, including progress bars and dynamic buttons.
- Provides a menu-driven interface for various functionalities.

---

#### **Requirements**
1. **ADB (Android Debug Bridge):**
   - Ensure ADB is installed and configured on your system.
   - Device debugging must be enabled, and the device should be connected via USB or Wi-Fi.

2. **Python 3.x**:
   - Required to run the script.

3. **Python Packages**:
   - No external libraries are needed (uses built-in Python libraries like `os`, `json`, and `argparse`).

4. **SafeUM App Installed**:
   - The target device should have the SafeUM app installed and accessible.

---

#### **Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/safeum-automation.git
   cd safeum-automation
   ```

2. Install ADB on your system:
   - For **Ubuntu**:
     ```bash
     sudo apt update
     sudo apt install adb
     ```
   - For **Windows**:
     Download the SDK Platform Tools from [here](https://developer.android.com/studio/releases/platform-tools).

3. Verify ADB installation:
   ```bash
   adb devices
   ```
   Ensure your device is listed.

4. Run the script:
   ```bash
   python safeum_automation.py
   ```

---

#### **Usage**
1. **Menu Options**:
   - Option 1: Automate the login, phone number extraction, and logout for multiple accounts.
   - Option 2: Display previously extracted accounts from a JSON file.
   - Option 3: Set up coordinates for UI elements (required for first-time setup).
   - Option 4: Exit the script.

2. **Setup Coordinates**:
   If running the script for the first time or on a new device, configure the coordinates for various UI elements using the interactive setup mode.

3. **Command-Line Arguments**:
   Use the `--setup` argument to specify a previously saved setup:
   ```bash
   python safeum_automation.py --setup <setup_name>
   ```

---

#### **Additional Tools**
- **UI Automator Viewer**:
  - Use this to identify the resource IDs or coordinates of UI elements for precise setup.
  - It is part of the Android SDK.

---

#### **Important Notes**
- The script modifies device state and interacts with applications. Use it responsibly.
- Ensure the `adb` commands work seamlessly on your system before running the script.
- Keep your ADB-connected device secure to avoid unauthorized access.

---

#### **Contributing**
Feel free to submit issues or pull requests to enhance the script further. Contributions are welcome!

---
