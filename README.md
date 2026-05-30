# SilentGuard AI 🛡️

**Behavioral Spyware & Anomaly Detection Suite**  
Cross-platform protection for Windows · macOS · Linux · Android  
using **AI (Autoencoders + Random Forest)** — no signature dependency

<br>

## 📌 What is SilentGuard AI?

SilentGuard AI is a **privacy-focused, open-source tool** that detects spyware, stalkerware and other stealth surveillance software by analyzing **behavior** instead of known file hashes.

It learns what "normal" looks like on **your** computer/phone and flags unusual patterns such as:

- unexpected CPU / memory / network spikes
- suspicious process behavior
- dangerous Android permission combinations
- abnormal sensor / background activity

<br>

## ✨ Main Features

- Zero-day & unknown spyware detection  
- Personalized AI model trained on **your** normal usage  
- Desktop: real-time process & resource monitoring (psutil)  
- Android: app list, dangerous permissions & ADB-based analysis  
- One adaptive dashboard (Streamlit) — works on PC and phone  
- Professional AI-generated threat notifications  
- Option to kill suspicious processes (desktop)  
- Cross-platform: Windows, macOS, Linux + Android

<br>

## 🚀 Quick Start (most users)

### 1. Clone repository
```bash
git clone https://github.com/YOUR_USERNAME/silentguard-ai.git
cd silentguard-ai
```

### 2. Create Virtual Environment
# Linux / macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

# Windows
python -m venv venv
```bash
.\venv\Scripts\activate
```

### 3. Install Dependencies
```Bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Train Your Personal AI Model (Recommended)

# Step 1 – Record normal usage (5–10 minutes)
python data_collector.py

# Step 2 – Normalize data
python prepare_data.py

# Step 3 – Train Autoencoder model
python train_model.py

### This generates:

autoencoder_model.pth

### 5. Run Application
# Recommended (shows IP automatically)
./run_app.sh

# OR manually
streamlit run app.py --server.address=0.0.0.0 --server.port=8501

### Open in browser:
http://localhost:8501
### Or from phone (same WiFi):
http://192.168.x.x:8501

# 📂 Project Structure
silentguard-ai/
│
├── app.py
├── run_app.sh
│
├── ai_engine.py
├── desktop_ai_model.py
│
├── desktop_security.py
├── android_monitor.py
│
├── notification_service.py
│
├── data_collector.py
├── prepare_data.py
├── train_model.py
│
├── requirements.txt
├── README.md
└── autoencoder_model.pth (generated)

# 🛠️ Full Setup Guide
### Requirements

- Python 3.9 – 3.11

### Git

- ADB (for Android scanning)

### Download ADB:
- https://developer.android.com/tools/releases/platform-tools

Add adb to system PATH.

# Setup Steps

- 1. Clone repository

- 2. Create virtual environment

- 3. Install dependencies

- 4. Train AI model (recommended)

- 5. (Optional) Setup Android:
      - Enable Developer Options
     -  Enable USB Debugging
     -  Run:
     -  - adb devices
- 6. Launch dashboard:
```Bash

- ./run_app.sh
```
# 🔧 Typical Usage
- ## Desktop Scan

    - Open dashboard

    - Click Scan Processes

    - Risk score > 70% highlighted

- ## Android Scan
   - Connect phone via USB / WiFi ADB

   - Click Scan Android

  - View apps + dangerous permissions

- ## Terminate Suspicious Process

   - Click Terminate

  - May require admin / sudo

# ⚠️ Notes & Limitations

- Not a replacement for commercial antivirus

- Best accuracy requires personal training

- Android requires active ADB connection

- Process termination requires elevated privileges

- CPU-only model (no GPU)

- Basic file scanning (can be improved)

# 🛠️ Troubleshooting
| Problem                  | Solution                       |
| ------------------------ | ------------------------------ |
| `adb not found`          | Install ADB and add to PATH    |
| No threats detected      | Train model first              |
| Too many false positives | Record longer normal usage     |
| Cannot open on phone     | Use `--server.address=0.0.0.0` |
| Torch errors             | Install CPU version            |
| Permission denied        | Run terminal as admin / sudo   |

# Install Torch CPU:
```Bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```
# 🔮 Future Improvements

- iOS limited monitoring (network behavior)

- Camera / microphone detection

- False-positive reduction

- Dark mode UI

- PDF / HTML security reports

- Multi-device shared AI model

# 📄 License

- MIT License — Free to use, modify, distribute.

# ❤️ Contributing

- Pull requests welcome, especially for:

- Improved AI models

- Android indicators

- UI/UX

- False-positive reduction

# 👨‍💻 Author

Dharmesh Vekaria
Anand, Gujarat · 2025–2026

Focused on privacy & modern behavioral threat detection.

# 🛡️ Stay Safe · Stay Private


---

If you want, I can next:

- Add **GitHub badges (build, license, Python, stars)**  
- Create **professional GitHub repo description + tags**  
- Write **research-paper style documentation**  
- Add **screenshots section for your UI**  
- Make **README look like a commercial security product page**  

Just say 👍
