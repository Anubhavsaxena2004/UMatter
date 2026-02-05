# ScoringScoring/utils/aggregator.py
import json
from django.conf import settings

ANSWER_MAP = {"A": 0, "B": 1, "C": 2, "D": 3}

QUESTIONS_PATH = settings.BASE_DIR / "ScoringScoring/ml/questions_ml.json"
with open(QUESTIONS_PATH) as f:
    QUESTIONS = json.load(f)

ID_TO_CATEGORY = {q["id"]: q["category"] for q in QUESTIONS}

def aggregate_scores(responses):
    buckets = {
        "Family": [],
        "Financial": [],
        "Career": [],
        "Love": []
    }

    for r in responses:
        cat = ID_TO_CATEGORY[r["id"]]
        buckets[cat].append(ANSWER_MAP[r["answer"]])

    return [
        sum(buckets["Family"]) / len(buckets["Family"]),
        sum(buckets["Financial"]) / len(buckets["Financial"]),
        sum(buckets["Career"]) / len(buckets["Career"]),
        sum(buckets["Love"]) / len(buckets["Love"]),
    ]
