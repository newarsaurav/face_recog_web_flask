from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import face_recognition
import json
import os

app = Flask(__name__)

FACE_DB = "faces.json"

def save_face(name, encoding):
    data = {}
    if os.path.exists(FACE_DB):
        with open(FACE_DB, "r") as f:
            data = json.load(f)
    
    data[name] = encoding.tolist()  # Convert numpy array to list
    
    with open(FACE_DB, "w") as f:
        json.dump(data, f)

# Function to load stored face encodings
def load_faces():
    if os.path.exists(FACE_DB):
        with open(FACE_DB, "r") as f:
            return json.load(f)
    return {}

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET' , 'POST'])
def register():
    if request.method == "POST" :
        if 'image' not in request.files:
            return jsonify({"status": "error", "message": "No image uploaded!"}), 400

        file = request.files['image']
        name = request.form.get('name')

        if not name:
            return jsonify({"status": "error", "message": "Name is required!"}), 400

        image = face_recognition.load_image_file(file)
        face_encodings = face_recognition.face_encodings(image)

        if face_encodings:
            save_face(name, face_encodings[0])
            return jsonify({"status": "success", "message": f"Face registered for {name}!"})
        else:
            return jsonify({"status": "error", "message": "No face detected!"}), 400

    else:
        return render_template('register.html')
    
    
@app.route('/login', methods=['POST'])
def login():
    if 'image' not in request.files:
        return jsonify({"status": "error", "message": "No image uploaded!"}), 400

    file = request.files['image']
    image = face_recognition.load_image_file(file)
    face_encodings = face_recognition.face_encodings(image)

    if not face_encodings:
        return jsonify({"status": "error", "message": "No face detected!"}), 400

    known_faces = load_faces()
    user_encoding = face_encodings[0]

    for name, encoding in known_faces.items():
        stored_encoding = np.array(encoding)
        match = face_recognition.compare_faces([stored_encoding], user_encoding, tolerance=0.5)

        if match[0]:
            return jsonify({"status": "success", "message": f"Welcome, {name}!"})

    return jsonify({"status": "error", "message": "Face not recognized!"}), 400


if __name__ == '__main__':
    app.run(debug=True)
