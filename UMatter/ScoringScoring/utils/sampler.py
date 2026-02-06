# ScoringScoring/utils/sampler.py
import json, random
from django.conf import settings

QUESTIONS_PATH = settings.BASE_DIR / "ScoringScoring/ml/questions_ui.json"

with open(QUESTIONS_PATH, encoding='utf-8') as f:
    data = json.load(f)
    # Parse the nested structure from questions_ui.json
    QUESTIONS = []
    for section in data["sections"]:
        category = section["name"].split()[0]  # "Family Trauma" -> "Family"
        for q in section["questions"]:
            QUESTIONS.append({
                "id": q["number"],
                "category": category,
                "text": q["text"],
                "options": q["options"]
            })

def get_random_questions():
    """Select 15 random questions: Family(4), Financial(4), Career(4), Love(3)"""
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