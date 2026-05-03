import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "models", "scaler.pkl")

JWT_SECRET = os.getenv('JWT_SECRET_KEY')
JWT_EXPIRY_HOURS = int(os.getenv('JWT_EXPIRY_HOURS', 24))
