# 🎙 EmoSense AI — Voice Emotion Detection

> Record your voice. Understand your emotion. Get intelligent feedback.

EmoSense AI is a full-stack machine learning web application that detects human emotions from voice recordings in real time. It uses a trained neural network on the RAVDESS dataset to classify 8 emotions from audio features extracted using Librosa. The system includes JWT-based authentication, MongoDB for persistent storage, and is deployed live on Railway.

---

## 🚀 Live Demo

🌐 **[https://emosenseai-production.up.railway.app](https://emosenseai-production.up.railway.app)**

---

## ✨ What's New

- ✅ JWT-based user authentication (register & login)
- ✅ MongoDB integration for storing user data and emotion history
- ✅ Per-user session history with date, time, and feedback
- ✅ Upload pre-recorded audio files (.wav, .mp3, .webm)
- ✅ Beautiful dashboard UI with live waveform animation
- ✅ Deployed on Railway — accessible 24/7

---

## 🧠 How It Works

1. User registers or logs in — receives a JWT token
2. User records voice via the browser microphone or uploads an audio file
3. Audio is sent to a Flask REST API with the JWT token in the request header
4. Middleware validates the token before processing the request
5. Backend extracts **MFCC**, **Chroma**, and **Mel Spectrogram** features using Librosa
6. Features are scaled and passed to a trained **MLPClassifier** neural network
7. Detected emotion and personalized AI feedback (via Gemini) are returned as JSON
8. Result is displayed on the dashboard and saved to MongoDB for history tracking

---

## 🎯 Model Performance

| Metric | Value |
|---|---|
| Dataset | RAVDESS (24 actors, 1440 audio files) |
| Features | MFCC (40) + Chroma (12) + Mel Spectrogram (128) = 180 features |
| Model | MLPClassifier — hidden layers (256, 128) |
| Accuracy | **72.92%** on 20% test split |
| Emotions | Neutral, Calm, Happy, Sad, Angry, Fearful, Disgust, Surprised |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript (Web Audio API) |
| Backend | Python, Flask, Flask-CORS |
| Authentication | JWT (PyJWT), bcrypt |
| Database | MongoDB Atlas (pymongo) |
| ML / Audio | Librosa, Scikit-learn, NumPy |
| Model | MLPClassifier (scikit-learn) |
| AI Feedback | Google Gemini API |
| Audio Processing | ffmpeg, pydub, soundfile |
| Deployment | Railway |

---

## 📁 Project Structure

```
emosense.ai/
├── app.py                   # Flask application entry point
├── config.py                # Path and environment configuration
├── db.py                    # MongoDB connection
├── requirements.txt         # Python dependencies
├── Procfile                 # Railway/Render deployment config
├── .env                     # Environment variables (not committed)
├── .gitignore
│
├── auth/
│   ├── __init__.py
│   ├── middleware.py        # JWT token validation decorator
│   ├── models.py            # User create, find, verify functions
│   └── routes.py            # /auth/register and /auth/login endpoints
│
├── models/
│   ├── model.pkl            # Trained MLPClassifier
│   └── scaler.pkl           # StandardScaler
│
├── services/
│   ├── emotion_service.py   # Prediction logic (lazy loaded)
│   └── feedback_service.py  # Gemini AI feedback generation
│
├── utils/
│   └── audio_features.py    # MFCC/Chroma/Mel extraction
│
├── static/
│   └── js/
│       └── main.js          # Frontend JavaScript (auth, recording, history)
│
├── templates/
│   └── index.html           # Dashboard UI
│
└── training/
    ├── train_model.py        # Model training script
    └── preprocessing.py      # Feature extraction from RAVDESS
```

---

## 🔐 Authentication Flow

```
Register  →  POST /auth/register  →  saves user to MongoDB (password hashed with bcrypt)
Login     →  POST /auth/login     →  verifies password → returns JWT token
Request   →  Authorization: Bearer <token>  →  middleware validates → allows access
History   →  GET /history         →  returns per-user emotion sessions from MongoDB
```

---

## ⚙️ Setup & Run Locally

### Prerequisites

- Python 3.10+
- ffmpeg installed (`brew install ffmpeg` on Mac)
- MongoDB running locally or a MongoDB Atlas connection string

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/sakibraza07/emosense.ai.git
cd emosense.ai

# 2. Install Python dependencies
pip3 install -r requirements.txt

# 3. Create a .env file with the following variables
MONGO_DB_URL=mongodb://localhost:27017/emosenseai
JWT_SECRET_KEY=your_secret_key_here
JWT_EXPIRY_HOURS=24
GOOGLE_GEMINI_API_KEY=your_gemini_api_key_here

# 4. Run the Flask server
python3 app.py

# 5. Open in browser
# Go to http://127.0.0.1:5001
```

---

## 🔁 Retrain the Model (Optional)

```bash
# Step 1 — Extract features from dataset
python3 training/preprocessing.py

# Step 2 — Train and save the model
python3 training/train_model.py
```

> ⚠️ The RAVDESS dataset is NOT included in this repo. Download it from [Zenodo](https://zenodo.org/record/1188976).

---

## 📡 API Endpoints

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/auth/register` | Register a new user | ❌ |
| POST | `/auth/login` | Login and receive JWT token | ❌ |
| GET | `/auth/me` | Get current user details | ✅ |
| POST | `/predict` | Analyze audio and detect emotion | ✅ |
| GET | `/history` | Get user's emotion session history | ✅ |

---

## 🌱 Future Improvements

- [ ] Multilingual support (Hindi + English auto-detection)
- [ ] Emotion trend charts and analytics dashboard
- [ ] Real-time streaming emotion detection
- [ ] Share emotion result cards
- [ ] Mobile-optimized UI
- [ ] Improve model accuracy with deep learning (CNN on spectrograms)

---

## 👤 Author

**Sakib Raza**
B.Tech Computer Science & Engineering
GitHub: [@sakibraza07](https://github.com/sakibraza07)
Portfolio: [sakibraza07.github.io](https://sakibraza07.github.io)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).