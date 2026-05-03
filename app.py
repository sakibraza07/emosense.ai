from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import tempfile
from datetime import datetime
from pydub import AudioSegment

from services.emotion_service import predict_emotion
from services.feedback_service import generate_feedback
from auth.routes import auth_bp
from auth.middleware import token_required
from db import history_collection

app = Flask(__name__)
CORS(app)
app.register_blueprint(auth_bp)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["GET","POST"])
@token_required
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

        # Extract user_id from token
        user_id = request.user_id

        # Build and insert history document
        history_doc = {
            "user_id": user_id,
            "emotion": emotion,
            "emotion_code": code,
            "feedback": feedback,
            "timestamp": datetime.utcnow()
        }
        history_collection.insert_one(history_doc)

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

@app.route("/history", methods=["GET"])
@token_required
def history():
    # Get user_id from token
    user_id = request.user_id
    
    # Find user's records from history_collection
    records = list(history_collection.find({"user_id": user_id}))
    
    # Convert ObjectId to string for JSON serialization
    for record in records:
        record["_id"] = str(record["_id"])
    
    return jsonify({"history": records})

if __name__ == "__main__":
    app.run(debug=True,port=5001)
