from django.http import JsonResponse
from .utils.sampler import get_random_questions
import json
from django.http import JsonResponse
from .utils.aggregator import aggregate_scores
from .utils.predictor import predict_trauma
from core.models import Question, TraumaType, UserAnswer, TraumaScore, DominantTrauma
from django.contrib.auth.models import User
from django.utils import timezone

def evaluate_test(request):
    """
    Legacy endpoint - now integrated with database
    """
    data = json.loads(request.body)
    responses = data["responses"]

    features = aggregate_scores(responses)
    prediction = predict_trauma(features)
    
    # Save to database if user_id is provided
    user_id = data.get('user_id', None)
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            
            # Save answers
            for response in responses:
                question_id = response.get('id')
                answer_value = response.get('answer')
                
                try:
                    question = Question.objects.get(id=question_id)
                    UserAnswer.objects.update_or_create(
                        user=user,
                        question=question,
                        defaults={'answer_value': answer_value}
                    )
                except Question.DoesNotExist:
                    continue
            
            # Save trauma scores
            trauma_types = TraumaType.objects.all()
            trauma_map = {
                'Family': trauma_types.filter(name='Family').first(),
                'Financial': trauma_types.filter(name='Financial').first(),
                'Career': trauma_types.filter(name='Career').first(),
                'Love': trauma_types.filter(name='Love').first(),
            }
            
            for trauma_name, score in zip(['Family', 'Financial', 'Career', 'Love'], features):
                trauma_type = trauma_map.get(trauma_name)
                if trauma_type:
                    # Determine severity level
                    if score < 1.0:
                        severity = 'low'
                    elif score < 1.5:
                        severity = 'moderate'
                    elif score < 2.0:
                        severity = 'high'
                    else:
                        severity = 'severe'
                    
                    TraumaScore.objects.create(
                        user=user,
                        trauma_type=trauma_type,
                        score_percentage=(score / 3.0) * 100,
                        severity_level=severity
                    )
            
            # Identify dominant trauma
            sorted_predictions = sorted(prediction.items(), key=lambda x: x[1], reverse=True)
            primary_trauma_name = sorted_predictions[0][0]
            secondary_trauma_name = sorted_predictions[1][0] if len(sorted_predictions) > 1 else None
            
            primary_trauma = trauma_map.get(primary_trauma_name)
            secondary_trauma = trauma_map.get(secondary_trauma_name) if secondary_trauma_name else None
            
            if primary_trauma:
                DominantTrauma.objects.update_or_create(
                    user=user,
                    defaults={
                        'primary_trauma': primary_trauma,
                        'secondary_trauma': secondary_trauma,
                        'confidence_score': sorted_predictions[0][1]
                    }
                )
        except User.DoesNotExist:
            pass

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
    """
    Legacy endpoint - now returns database questions
    Falls back to sampler if database is empty
    """
    # Try to get questions from database
    db_questions = Question.objects.all().order_by('trauma_type', 'order')
    
    if db_questions.exists():
        # Return database questions in the expected format
        questions_list = []
        for q in db_questions:
            questions_list.append({
                'id': q.id,
                'text': q.question_text,
                'options': [
                    'Never / Strongly Disagree',
                    'Rarely / Disagree',
                    'Often / Agree',
                    'Always / Strongly Agree'
                ],
                'trauma_type': q.trauma_type.name
            })
        return JsonResponse({"questions": questions_list})
    else:
        # Fallback to old sampler
        questions = get_random_questions()
        return JsonResponse({"questions": questions})

