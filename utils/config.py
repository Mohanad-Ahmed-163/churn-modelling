from dotenv import load_dotenv
import os
import joblib
load_dotenv(override=True)  
# Load environment variables from .env file
APP_NAME = os.getenv("APP_NAME")
VERSION = os.getenv("VERSION")
SECRET_KEY = os.getenv("SECRET_KEY")


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_FOLDER_PATH = os.path.join(BASE_DIR, 'models')

#Models
forest_tuned = joblib.load(os.path.join(MODELS_FOLDER_PATH, 'forest_tuned.pkl'))
preprocessor = joblib.load(os.path.join(MODELS_FOLDER_PATH, 'preprocessor.pkl'))
xgboost_tuned = joblib.load(os.path.join(MODELS_FOLDER_PATH, 'xgb-tuned.pkl'))
