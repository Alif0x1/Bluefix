#!/usr/bin/env python3

import subprocess
from time import sleep

def check_bluetooth_service():
    bluetooth_status = subprocess.run(["systemctl", "is-active", "bluetooth"], capture_output=True, text=True).stdout.strip()
    if bluetooth_status != "active":
        print("Bluetooth service is not running. Starting it...")
        subprocess.run(["sudo", "systemctl", "start", "bluetooth"])
        sleep(2)

def check_bluetooth_adapter():
    adapter_status = subprocess.run(["rfkill", "list", "bluetooth"], capture_output=True, text=True).stdout
    if "Soft blocked: yes" in adapter_status:
        print("Bluetooth adapter is blocked. Unblocking it...")
        subprocess.run(["sudo", "rfkill", "unblock", "bluetooth"])
        sleep(2)

def restart_bluetooth_service():
    print("Restarting Bluetooth service...")
    subprocess.run(["sudo", "systemctl", "restart", "bluetooth"])
    sleep(2)

def check_bluetooth_device():
    device_count = subprocess.run(["hciconfig"], capture_output=True, text=True).stdout.count("hci")
    if device_count == 0:
        print("No Bluetooth device found. Make sure it is properly connected.")
        return False
    return True

def enable_bluetooth_discoverability():
    print("Enabling Bluetooth discoverability...")
    subprocess.run(["sudo", "hciconfig", "hci0", "piscan"])

def fix_bluetooth_issues():
    check_bluetooth_service()
    check_bluetooth_adapter()
    restart_bluetooth_service()
    if not check_bluetooth_device():
        return
    enable_bluetooth_discoverability()

    print("Bluetooth troubleshooting completed.")

if __name__ == "__main__":
    fix_bluetooth_issues()

