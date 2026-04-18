# 🔐 PhishShield

A cybersecurity tool that detects phishing URLs using rule-based analysis, real-time threat intelligence, and a hacker-style GUI.

---

## 🚀 Features

* 🧠 Rule-based phishing detection
* 🌐 Integration with VirusTotal API
* 🖥️ Hacker-style GUI (Tkinter)
* 🔍 URL validation (prevents invalid scans)
* 📊 Real-time scan results
* ⚡ Lightweight and easy to use

---


---


---

## 🛠️ Tech Stack

* Python
* Tkinter
* Selenium
* Requests
* VirusTotal API

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/kaaliya123/PhishShield.git
cd PhishShield
```

---

### 2️⃣ Install dependencies

```bash
pip install requests selenium webdriver-manager python-dotenv
```

---

### 3️⃣ Setup environment variables

Create a `.env` file in the root folder:

```env
VT_API_KEY=your_api_key_here
```

---

### 4️⃣ Run the application

```bash
python main.py
```

---

## 🧪 Test URLs

Use these URLs to test the tool:

* https://example.com
* http://testphp.vulnweb.com
* https://google.com

---

## ⚠️ Important Notes

* `.env` file is not included for security reasons
* Free VirusTotal API has request limits
* Some fake domains may not load (handled safely in code)

---

## 📌 Future Improvements

* 📸 Show screenshot preview inside GUI
* 📊 Add scan history tracking
* 📄 Generate PDF reports
* 🧠 AI-based phishing detection

---

## 👨‍💻 Author

**Saksham Bhawaniya**

---

## ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub!
