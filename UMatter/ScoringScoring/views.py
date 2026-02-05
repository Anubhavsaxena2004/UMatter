from django.http import JsonResponse
from .utils.sampler import get_random_questions
import json
from django.http import JsonResponse
from .utils.aggregator import aggregate_scores
from .utils.predictor import predict_trauma

def evaluate_test(request):
    data = json.loads(request.body)
    responses = data["responses"]

    features = aggregate_scores(responses)
    prediction = predict_trauma(features)

    return JsonResponse({
        "features": {
            "Family": features[0],
            "Financial": features[1],
            "Career": features[2],
            "Love": features[3],
        },
        "prediction": prediction
    })

def get_questions(request):
    questions = get_random_questions()
    return JsonResponse({"questions": questions})
