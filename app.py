import cv2
import face_recognition
import pickle
import numpy as np
from flask import Flask, render_template, Response
import time
from datetime import datetime

app = Flask(__name__)

# Load the known faces and encodings from the backend folder
ENCODINGS_PATH = "backend/encodings.pickle"

try:
    with open(ENCODINGS_PATH, "rb") as f:
        data = pickle.load(f)
    known_encodings = data["encodings"]
    known_names = data["names"]
    print(f"[*] Loaded {len(known_names)} face encodings.")
except FileNotFoundError:
    print(f"[!] Error: {ENCODINGS_PATH} not found. Please run backend/encode_faces.py first.")
    known_encodings = []
    known_names = []

# Global list to store logs for the web dashboard (Server-Sent Events)
logs_queue = []

def generate_frames():
    """Video streaming generator function."""
    camera = cv2.VideoCapture(0)
    
    # Track people seen recently to avoid duplicate logs in a short window (10 seconds cooldown)
    seen_timeout = {} 
    
    while True:
        success, frame = camera.read()
        if not success:
            break
        
        # Resize frame to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Unknown"

            # Use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_names[best_match_index]

            # Logging logic: only log if person is known and hasn't been seen in the last 10 seconds
            current_time = time.time()
            if name != "Unknown":
                if name not in seen_timeout or (current_time - seen_timeout[name]) > 10:
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    log_entry = f"[{timestamp}] Identified: {name}"
                    logs_queue.append(log_entry)
                    seen_timeout[name] = current_time
                    print(f"[+] {log_entry}")

            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top, right, bottom, left = face_location
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.8, (255, 255, 255), 1)

        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        
        # Yield the output frame in the byte format required for MJPEG stream
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    """Main dashboard home page."""
    return render_template('index.html')

@app.route('/security')
def security():
    """Security feed page."""
    return render_template('stream.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/logs')
def stream_logs():
    """Server-Sent Events endpoint for real-time face logs."""
    def event_stream():
        while True:
            if logs_queue:
                log_item = logs_queue.pop(0)
                yield f"data: {log_item}\n\n"
            time.sleep(0.5)
    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == "__main__":
    print("[*] Starting School Surveillance Server...")
    print("[*] Dashboard available at: http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
