import requests
import base64
import time
import os
import socket
from urllib.parse import urlparse
import tkinter as tk
from tkinter import messagebox

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from dotenv import load_dotenv

# -------------------------------
# LOAD ENV VARIABLES
# -------------------------------
load_dotenv()
API_KEY = os.getenv("VT_API_KEY")

# -------------------------------
# URL VALIDATION
# -------------------------------
def is_valid_domain(url):
    try:
        parsed = urlparse(url)
        domain = parsed.netloc
        if not domain:
            return False
        socket.gethostbyname(domain)
        return True
    except:
        return False


# -------------------------------
# RULE-BASED CHECK
# -------------------------------
def rule_based_check(url):
    score = 0

    if "@" in url:
        score += 2
    if url.startswith("http://"):
        score += 2
    if "-" in url:
        score += 1
    if len(url) > 30:
        score += 1

    if score >= 3:
        return "Phishing"
    elif score == 2:
        return "Suspicious"
    else:
        return "Safe"


# -------------------------------
# VIRUSTOTAL CHECK
# -------------------------------
def check_virustotal(url):
    if not API_KEY or not is_valid_domain(url):
        return "Unknown"

    try:
        encoded_url = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
        vt_url = f"https://www.virustotal.com/api/v3/urls/{encoded_url}"

        headers = {"x-apikey": API_KEY}
        response = requests.get(vt_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            malicious = data["data"]["attributes"]["last_analysis_stats"]["malicious"]
            return "Phishing" if malicious > 0 else "Safe"
        else:
            print("VT Error:", response.status_code)
            return "Unknown"

    except Exception as e:
        print("VT Exception:", e)
        return "Error"


# -------------------------------
# SCREENSHOT (FINAL FIXED VERSION)
# -------------------------------
def capture_screenshot(url):
    if not is_valid_domain(url):
        return "Invalid URL"

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = None

    try:
        print("🚀 Launching browser...")

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

        print("🌐 Opening:", url)

        driver.set_page_load_timeout(20)
        driver.get(url)

        time.sleep(5)

        folder = os.path.join(os.getcwd(), "screenshots")
        if not os.path.exists(folder):
            os.makedirs(folder)

        filename = url.replace("https://", "").replace("http://", "").replace("/", "_")
        filepath = os.path.join(folder, f"{filename}.png")

        success = driver.save_screenshot(filepath)

        if success:
            print("📸 Saved:", filepath)
            return filepath
        else:
            return "Screenshot Failed"

    except Exception as e:
        print("Screenshot Error:", e)
        return "Error"

    finally:
        if driver:
            driver.quit()


# -------------------------------
# SCAN FUNCTION (GUI)
# -------------------------------
def scan_url():
    url = entry.get()

    if not url:
        messagebox.showwarning("Error", "Enter a URL")
        return

    result_box.config(state="normal")
    result_box.delete(1.0, tk.END)

    result_box.insert(tk.END, ">> Initializing Scan...\n")
    root.update()

    rule = rule_based_check(url)
    result_box.insert(tk.END, f">> Rule Engine: {rule}\n")

    vt = check_virustotal(url)
    result_box.insert(tk.END, f">> VirusTotal: {vt}\n")

    screenshot = capture_screenshot(url)
    result_box.insert(tk.END, f">> Screenshot: {screenshot}\n")

    if rule == "Phishing" or vt == "Phishing":
        final = "🚨 PHISHING DETECTED"
    elif rule == "Suspicious":
        final = "⚠️ SUSPICIOUS"
    else:
        final = "✅ SAFE"

    result_box.insert(tk.END, f"\n>> FINAL RESULT: {final}\n")
    result_box.config(state="disabled")


# -------------------------------
# GUI DESIGN (HACKER STYLE)
# -------------------------------
root = tk.Tk()
root.title("CyberScan Terminal")
root.geometry("650x420")
root.configure(bg="black")

title = tk.Label(
    root,
    text=">>> CYBER PHISHING DETECTOR <<<",
    fg="#00FF00",
    bg="black",
    font=("Courier", 16, "bold")
)
title.pack(pady=10)

entry = tk.Entry(
    root,
    width=70,
    bg="black",
    fg="#00FF00",
    insertbackground="#00FF00",
    font=("Courier", 10)
)
entry.pack(pady=10)

scan_btn = tk.Button(
    root,
    text="[ RUN SCAN ]",
    command=scan_url,
    bg="black",
    fg="#00FF00",
    activebackground="#003300",
    font=("Courier", 10, "bold"),
    bd=1
)
scan_btn.pack(pady=10)

result_box = tk.Text(
    root,
    height=12,
    width=80,
    bg="black",
    fg="#00FF00",
    insertbackground="#00FF00",
    font=("Courier", 10)
)
result_box.pack(pady=10)
result_box.config(state="disabled")

root.mainloop()