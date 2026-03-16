import pickle
import os
from utils.audio_features import extract_features

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model = pickle.load(open(os.path.join(BASE_DIR, "models/model.pkl"), "rb"))
scaler = pickle.load(open(os.path.join(BASE_DIR, "models/scaler.pkl"), "rb"))

emotion_map = {
    "01": "neutral", "02": "calm", "03": "happy",
    "04": "sad", "05": "angry", "06": "fearful",
    "07": "disgust", "08": "surprised"
}

def predict_emotion(file_path):
    features = extract_features(file_path)
    features = features.reshape(1, -1)
    features = scaler.transform(features)

    prediction = model.predict(features)[0]
    prediction_str = str(prediction).zfill(2)

    return emotion_map.get(prediction_str, "unknown"), prediction_str
