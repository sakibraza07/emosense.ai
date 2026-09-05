# 🎙 EmoSense AI — Voice Emotion Detection

> Record your voice. Understand your emotion. Get intelligent feedback.

EmoSense AI is a full-stack machine learning web application that detects human emotions from voice recordings in real time. It uses an SVM classifier trained on the RAVDESS dataset to classify 8 emotions from a rich set of audio features extracted using Librosa. The system includes JWT-based authentication, MongoDB for persistent storage, and is deployed live on Render.

---

## 🚀 Live Demo

🌐 **[https://emosense-ai-wscy.onrender.com](https://emosense-ai-wscy.onrender.com)**

> Hosted on Render's free tier — the app spins down after periods of inactivity, so the first request after a while may take 30-50s to wake up.

---

## ✨ What's New

- ✅ JWT-based user authentication (register & login)
- ✅ MongoDB integration for storing user data and emotion history
- ✅ Per-user session history with date, time, and feedback
- ✅ Upload pre-recorded audio files (.wav, .mp3, .webm)
- ✅ Beautiful dashboard UI with live waveform animation
- ✅ Deployed on Render via Docker
- ✅ Retrained with a richer 269-feature set, data augmentation, and cross-validated model selection — accuracy up from 72.92% to 83.33%

---

## 🧠 How It Works

1. User registers or logs in — receives a JWT token
2. User records voice via the browser microphone or uploads an audio file
3. Audio is sent to a Flask REST API with the JWT token in the request header
4. Middleware validates the token before processing the request
5. Backend extracts **MFCC (+ delta/delta-delta)**, **Chroma**, **log-scaled Mel Spectrogram**, **spectral contrast**, **zero-crossing rate**, and **RMS energy** using Librosa (269 features total)
6. Features are scaled and passed to a trained **SVM (RBF kernel)** classifier, selected via cross-validation over MLP, SVM, and Random Forest candidates
7. Detected emotion and personalized AI feedback (via Gemini) are returned as JSON
8. Result is displayed on the dashboard and saved to MongoDB for history tracking

---

## 🎯 Model Performance

| Metric | Value |
|---|---|
| Dataset | RAVDESS (24 actors, 1440 audio files), 4x'd via augmentation (noise, pitch shift, time stretch) to 5,760 training examples |
| Features | MFCC + delta + delta-delta (120) + Chroma (12) + log-Mel Spectrogram (128) + spectral contrast (7) + ZCR (1) + RMS (1) = 269 features |
| Model | SVM (RBF kernel, C=50) — selected via 5-fold cross-validation over MLP, SVM, and Random Forest |
| Accuracy | **83.33%** on held-out 20% test split (up from 72.92% on the original 180-feature MLP) |
| Emotions | Neutral, Calm, Happy, Sad, Angry, Fearful, Disgust, Surprised |

<details>
<summary>Per-class performance</summary>

| Emotion | Precision | Recall | F1-score |
|---|---|---|---|
| Neutral | 0.79 | 0.69 | 0.74 |
| Calm | 0.76 | 0.91 | 0.83 |
| Happy | 0.81 | 0.82 | 0.81 |
| Sad | 0.76 | 0.76 | 0.76 |
| Angry | 0.92 | 0.86 | 0.89 |
| Fearful | 0.85 | 0.90 | 0.88 |
| Disgust | 0.87 | 0.82 | 0.84 |
| Surprised | 0.91 | 0.84 | 0.87 |

Neutral is the weakest class — RAVDESS has fewer neutral samples than other emotions.
</details>

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript (Web Audio API) |
| Backend | Python, Flask, Flask-CORS |
| Authentication | JWT (PyJWT), bcrypt |
| Database | MongoDB Atlas (pymongo) |
| ML / Audio | Librosa, Scikit-learn, NumPy |
| Model | SVM — RBF kernel (scikit-learn) |
| AI Feedback | Google Gemini API |
| Audio Processing | ffmpeg, pydub, soundfile |
| Deployment | Render (Docker) |

---

## 📁 Project Structure

```
emosense.ai/
├── app.py                   # Flask application entry point
├── config.py                # Path and environment configuration
├── db.py                    # MongoDB connection
├── requirements.txt         # Python dependencies
├── Procfile                 # Gunicorn start command
├── Dockerfile               # Render deployment config
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
│   ├── model.pkl            # Trained SVM classifier
│   └── scaler.pkl           # StandardScaler
│
├── services/
│   ├── emotion_service.py   # Prediction logic (lazy loaded)
│   └── feedback_service.py  # Gemini AI feedback generation
│
├── utils/
│   └── audio_features.py    # Shared feature extraction (used by both training and inference)
│
├── static/
│   └── js/
│       └── main.js          # Frontend JavaScript (auth, recording, history)
│
├── templates/
│   └── index.html           # Dashboard UI
│
└── training/
    ├── train_model.py        # Cross-validates MLP/SVM/RandomForest, grid-searches the winner
    └── preprocessing.py      # Builds features.npy/labels.npy from RAVDESS, with augmentation
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
# Step 1 — Extract features from dataset (pass the path to the unzipped
# Audio_Speech_Actors_01-24 folder). Includes 4x data augmentation by default.
python3 training/preprocessing.py /path/to/Audio_Speech_Actors_01-24

# Step 2 — Cross-validates MLP/SVM/RandomForest, grid-searches the winner,
# and saves model.pkl + scaler.pkl
python3 training/train_model.py

# Step 3 — Move the new model files into place
mv model.pkl scaler.pkl models/
```

> ⚠️ The RAVDESS dataset is NOT included in this repo. Download **`Audio_Speech_Actors_01-24.zip`** (audio-only, ~200MB — not the full audio-video set) from [Zenodo](https://zenodo.org/record/1188976).

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
- [ ] Further accuracy gains with a CNN trained directly on raw spectrograms (current approach uses averaged hand-crafted features)

---

## 👤 Author

**Sakib Raza**
B.Tech Computer Science & Engineering
GitHub: [@sakibraza07](https://github.com/sakibraza07)
Portfolio: [sakibraza07.github.io](https://sakibraza07.github.io)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).