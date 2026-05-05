import cv2
import numpy as np
import os
import sys
from keras.models import model_from_json

# Get image path from command line
if len(sys.argv) < 2:
    print("Error: No image path provided.")
    sys.exit(1)

img_path = sys.argv[1]

# Load the model
json_path = os.path.join(os.path.dirname(__file__), "emotiondetector.json")
with open(json_path, "r") as json_file:
    model_json = json_file.read()
model = model_from_json(model_json)

model_path = os.path.join(os.path.dirname(__file__), 'emotiondetector.h5')
model.load_weights(model_path)

# Function to extract features from the image
def extract_features(image):
    feature = np.array(image)
    feature = feature.reshape(1, 48, 48, 1)
    return feature / 255.0

# Labels for emotions
labels = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}

# Check if the image exists
if not os.path.exists(img_path):
    print("Image not found")
    sys.exit(1)

img = cv2.imread(img_path)
img = cv2.resize(img, (600, int(600 * img.shape[0] / img.shape[1])))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.equalizeHist(gray)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))

if len(faces) == 0:
    print("neutral")  # default if no face found
else:
    for (x, y, w, h) in faces:
        face = gray[y:y + h, x:x + w]
        face = cv2.resize(face, (48, 48))
        face = extract_features(face)

        pred = model.predict(face, verbose=0)
        emotion = labels[pred.argmax()]
        print(emotion)
        break  # process only the first face
