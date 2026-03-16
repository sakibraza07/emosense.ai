from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import tempfile
from pydub import AudioSegment

from services.emotion_service import predict_emotion
from services.feedback_service import generate_feedback

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    uploaded_file = request.files["file"]

    if uploaded_file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    temp_webm = None
    temp_wav = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
            temp_webm = tmp.name
            uploaded_file.save(temp_webm)

        temp_wav = temp_webm.replace(".webm", ".wav")

        audio = AudioSegment.from_file(temp_webm)
        audio.export(temp_wav, format="wav")

        emotion, code = predict_emotion(temp_wav)
        feedback = generate_feedback(emotion)

        return jsonify({
            "emotion": emotion,
            "emotion_code": code,
            "feedback": feedback
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if temp_webm and os.path.exists(temp_webm):
            os.remove(temp_webm)
        if temp_wav and os.path.exists(temp_wav):
            os.remove(temp_wav)

if __name__ == "__main__":
    app.run(debug=True)
