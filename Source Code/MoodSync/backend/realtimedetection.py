import cv2
import numpy as np
from keras.models import model_from_json
import time
import os
import pygame  # for playing songs

# Load model
model = model_from_json(open("c:/EmoVerse/backend/emotiondetector.json", "r").read())
model.load_weights("c:/EmoVerse/backend/emotiondetector.h5")

# Face detection
haar_file = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(haar_file)

# Emotion labels and song paths
labels = {0 : 'angry', 1 : 'disgust', 2 : 'fear', 3 : 'happy', 4 : 'neutral', 5 : 'sad', 6 : 'surprise'}
emotion_to_song = {
    'angry': 'songs/angry.mp3',
    'disgust': 'songs/disgust.mp3',
    'fear': 'songs/fear.mp3',
    'happy': 'songs/happy.mp3',
    'neutral': 'songs/neutral.mp3',
    'sad': 'songs/sad.mp3',
    'surprise': 'songs/surprise.mp3'
}

def extract_features(image):
    feature = np.array(image)
    feature = feature.reshape(1,48,48,1)
    return feature / 255.0

# Start webcam
webcam = cv2.VideoCapture(0)
detected_emotion = None

while True:
    _, frame = webcam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        for (x,y,w,h) in faces:
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (48,48))
            face = extract_features(face)
            prediction = model.predict(face)
            detected_emotion = labels[prediction.argmax()]
            print(f"Detected Emotion: {detected_emotion}")
            webcam.release()
            cv2.destroyAllWindows()
            break
    if detected_emotion:
        break

# Play song
if detected_emotion in emotion_to_song:
    song_path = emotion_to_song[detected_emotion]
    if os.path.exists(song_path):
        print(f"Playing song for: {detected_emotion}")
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(1)
    else:
        print(f"Song file not found for emotion: {detected_emotion}")
else:
    print("No emotion detected.")
