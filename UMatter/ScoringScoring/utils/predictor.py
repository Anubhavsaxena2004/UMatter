# ScoringScoring/utils/predictor.py
import joblib
from django.conf import settings

MODEL_PATH = settings.BASE_DIR / "ScoringScoring/ml/trauma_model.pkl"
model = joblib.load(MODEL_PATH)

def predict_trauma(features):
    probs = model.predict_proba([features])[0]
    return dict(zip(model.classes_, probs))
