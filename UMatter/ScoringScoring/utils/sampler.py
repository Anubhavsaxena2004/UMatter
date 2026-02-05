# ScoringScoring/utils/sampler.py
import json, random
from django.conf import settings

QUESTIONS_PATH = settings.BASE_DIR / "ScoringScoring/ml/questions_ml.json"

with open(QUESTIONS_PATH) as f:
    QUESTIONS = json.load(f)

def get_random_questions():
    selected = []

    for cat, n in {
        "Family": 4,
        "Financial": 4,
        "Career": 4,
        "Love": 3
    }.items():
        selected.extend(
            random.sample(
                [q for q in QUESTIONS if q["category"] == cat],
                n
            )
        )

    random.shuffle(selected)
    return selected

def get_random_question():
    return random.choice(QUESTIONS)