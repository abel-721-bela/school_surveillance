# 🎓 School Surveillance System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask-lightgrey.svg)](https://flask.palletsprojects.com/)
[![Face Recognition](https://img.shields.io/badge/AI-Face--Recognition-green.svg)](https://github.com/ageitgey/face_recognition)

A professional, real-time facial recognition surveillance system designed for school environments. This system identifies students and staff from a live camera feed and logs their presence on a sleek, web-based dashboard.

---

## 🚀 Features

- **Real-Time Monitoring**: Low-latency video streaming with AI-powered face overlays.
- **Smart Identification**: Instantly recognizes known individuals and marks unknown faces.
- **Live Security Logs**: Real-time activity log using Server-Sent Events (SSE).
- **Automated Encodings**: Easy-to-use script for processing new face data.
- **Optimized Performance**: Multi-threaded processing and frame resizing for high FPS.

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Computer Vision**: OpenCV, Dlib
- **AI Model**: `face_recognition` (HOG/CNN based)
- **Frontend**: HTML5, CSS3 (Glassmorphism design), JavaScript (SSE)

---

## 📂 Setup Instructions

### 1. Prerequisites
Ensure you have Python 3.8+ installed. It is recommended to use a virtual environment.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Creating the Face Database
For the system to recognize people, you must set up the `known_faces` folder:

1.  **Create a folder** named `known_faces` in the root directory.
2.  **Add Images**: Place clear photos of individuals inside this folder.
3.  **Naming Convention**: Save the images with the person's name (e.g., `John_Doe.jpg` or `Jane_Smith.png`). The system uses the filename as the display name.

### 4. Generate Encodings
Once your images are ready, run the encoding script to process the biometric data:
```bash
python backend/encode_faces.py
```

### 5. Launch the System
Start the web dashboard:
```bash
python app.py
```
Visit `http://127.0.0.1:5000` in your browser to view the security feed.

---

## 🔒 Privacy & Security
This system is designed for local use. For privacy reasons, ensure that you have consent before processing facial data. The `known_faces` folder is ignored by Git in this repository to prevent the accidental upload of personal biometric data.

## 📄 License
This project is for educational and security research purposes.
