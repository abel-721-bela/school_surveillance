# backend/encode_faces.py

import os
import cv2
import face_recognition
import pickle

def encode_faces(folder_path='known_faces'):
    known_encodings = []
    known_names = []

    for image_name in os.listdir(folder_path):
        if not image_name.lower().endswith((".jpg", ".png", ".jpeg")):
            continue

        image_path = os.path.join(folder_path, image_name)
        image = cv2.imread(image_path)
        if image is None:
            print(f"[!] Couldn't read image: {image_path}")
            continue

        name = os.path.splitext(image_name)[0]  # filename without extension

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model='hog')
        encodings = face_recognition.face_encodings(rgb, boxes)

        for encoding in encodings:
            known_encodings.append(encoding)
            known_names.append(name)

    data = {"encodings": known_encodings, "names": known_names}
    with open("backend/encodings.pickle", "wb") as f:
        pickle.dump(data, f)

    print("[+] Encodings saved to backend/encodings.pickle")

if __name__ == "__main__":
    encode_faces()
