# ScoringScoring/utils/aggregator.py
import json
from django.conf import settings

# Map option text to scores
ANSWER_MAP = {
    "A": 0,  # Never / Not at all
    "B": 1,  # Sometimes / Slightly
    "C": 2,  # Often / Moderately
    "D": 3   # Always / Severely
}

QUESTIONS_PATH = settings.BASE_DIR / "ScoringScoring/ml/questions_ui.json"
with open(QUESTIONS_PATH, encoding='utf-8') as f:
    data = json.load(f)
    # Build ID to category mapping
    ID_TO_CATEGORY = {}
    for section in data["sections"]:
        category = section["name"].split()[0]  # "Family Trauma" -> "Family"
        for q in section["questions"]:
            ID_TO_CATEGORY[q["number"]] = category

def aggregate_scores(responses):
    """
    Calculate average scores per category from user responses.
    
    Args:
        responses: List of {id: int, answer: str} objects
        
    Returns:
        List of 4 floats: [Family, Financial, Career, Love] averages
    """
    buckets = {
        "Family": [],
        "Financial": [],
        "Career": [],
        "Love": []
    }

    for r in responses:
        cat = ID_TO_CATEGORY[r["id"]]
        score = ANSWER_MAP[r["answer"]]
        buckets[cat].append(score)

    # Calculate averages, handle empty buckets
    return [
        sum(buckets["Family"]) / len(buckets["Family"]) if buckets["Family"] else 0,
        sum(buckets["Financial"]) / len(buckets["Financial"]) if buckets["Financial"] else 0,
        sum(buckets["Career"]) / len(buckets["Career"]) if buckets["Career"] else 0,
        sum(buckets["Love"]) / len(buckets["Love"]) if buckets["Love"] else 0,
    ]
