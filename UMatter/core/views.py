from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
import json
from datetime import datetime, timedelta

from .models import (
    UserProfile, TraumaType, Question, UserAnswer,
    TraumaScore, DominantTrauma, RecoveryProgram, RecoveryStep,
    UserRecoveryProgress, Consultant, GovtScheme, HeritageContent,
    ModernProgressContent, MoodLog, Alert
)

# Import existing ML logic
from ScoringScoring.utils.aggregator import aggregate_scores
from ScoringScoring.utils.predictor import predict_trauma


# ============================================================================
# ASSESSMENT FLOW
# ============================================================================

@csrf_exempt
def get_questions_api(request):
    """Get all assessment questions organized by trauma type"""
    try:
        questions_data = []
        trauma_types = TraumaType.objects.all()
        
        for trauma_type in trauma_types:
            questions = Question.objects.filter(trauma_type=trauma_type).order_by('order')
            for q in questions:
                questions_data.append({
                    'id': q.id,
                    'trauma_type': trauma_type.name,
                    'text': q.question_text,
                    'weight': q.weight,
                    'is_critical': q.is_critical,
                    'order': q.order
                })
        
        return JsonResponse({'questions': questions_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def evaluate_assessment(request):
    """
    Evaluate user responses and calculate trauma scores
    Integrates with existing ML logic
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        data = json.loads(request.body)
        responses = data.get('responses', [])
        user_id = data.get('user_id', None)  # Optional for anonymous users
        
        # Get or create user (for now, allow anonymous)
        user = None
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                pass
        
        # Save answers if user is logged in
        if user:
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
        
        # Calculate scores using existing ML logic
        features = aggregate_scores(responses)
        prediction = predict_trauma(features)
        
        # Save trauma scores if user is logged in
        if user:
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
                        score_percentage=(score / 3.0) * 100,  # Convert to percentage
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
        
        return JsonResponse({
            'features': {
                'Family': features[0],
                'Financial': features[1],
                'Career': features[2],
                'Love': features[3],
            },
            'prediction': prediction
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ============================================================================
# RECOVERY PLANS
# ============================================================================

@csrf_exempt
def get_recovery_plan(request):
    """Get personalized recovery plan based on user's dominant trauma"""
    try:
        user_id = request.GET.get('user_id')
        if not user_id:
            return JsonResponse({'error': 'user_id required'}, status=400)
        
        user = User.objects.get(id=user_id)
        dominant_trauma = DominantTrauma.objects.filter(user=user).first()
        
        if not dominant_trauma:
            return JsonResponse({'error': 'No assessment found. Please complete assessment first.'}, status=404)
        
        # Get recovery program for primary trauma
        program = RecoveryProgram.objects.filter(
            trauma_type=dominant_trauma.primary_trauma,
            is_active=True
        ).first()
        
        if not program:
            return JsonResponse({'error': 'No recovery program available'}, status=404)
        
        # Get all steps
        steps = RecoveryStep.objects.filter(program=program).order_by('day_number')
        
        # Get user progress
        progress_map = {}
        user_progress = UserRecoveryProgress.objects.filter(user=user, step__program=program)
        for progress in user_progress:
            progress_map[progress.step.id] = {
                'status': progress.status,
                'completed_at': progress.completed_at.isoformat() if progress.completed_at else None
            }
        
        steps_data = []
        for step in steps:
            steps_data.append({
                'id': step.id,
                'day_number': step.day_number,
                'activity_type': step.activity_type,
                'title': step.title,
                'content': step.content,
                'resources': step.resources,
                'estimated_duration_minutes': step.estimated_duration_minutes,
                'progress': progress_map.get(step.id, {'status': 'not_started', 'completed_at': None})
            })
        
        return JsonResponse({
            'program': {
                'id': program.id,
                'title': program.title,
                'description': program.description,
                'duration_days': program.duration_days,
                'difficulty_level': program.difficulty_level,
                'trauma_type': dominant_trauma.primary_trauma.name
            },
            'steps': steps_data
        })
    
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def update_recovery_progress(request):
    """Update user's progress on a recovery step"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        step_id = data.get('step_id')
        status = data.get('status', 'completed')
        notes = data.get('notes', '')
        
        user = User.objects.get(id=user_id)
        step = RecoveryStep.objects.get(id=step_id)
        
        progress, created = UserRecoveryProgress.objects.update_or_create(
            user=user,
            step=step,
            defaults={
                'status': status,
                'completed_at': timezone.now() if status == 'completed' else None,
                'notes': notes
            }
        )
        
        return JsonResponse({
            'success': True,
            'progress': {
                'status': progress.status,
                'completed_at': progress.completed_at.isoformat() if progress.completed_at else None
            }
        })
    
    except (User.DoesNotExist, RecoveryStep.DoesNotExist) as e:
        return JsonResponse({'error': str(e)}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ============================================================================
# HERITAGE & MODERN CONTENT
# ============================================================================

@csrf_exempt
def get_heritage_content(request, trauma_type_name):
    """Get heritage content for a specific trauma type"""
    try:
        trauma_type = TraumaType.objects.get(name=trauma_type_name)
        heritage_content = HeritageContent.objects.filter(trauma_type=trauma_type)
        
        content_data = []
        for content in heritage_content:
            content_data.append({
                'id': content.id,
                'title': content.title,
                'historical_context': content.historical_context,
                'practice': content.practice,
                'relevance_today': content.relevance_today,
                'source': content.source
            })
        
        return JsonResponse({'heritage_content': content_data})
    
    except TraumaType.DoesNotExist:
        return JsonResponse({'error': 'Trauma type not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def get_modern_content(request, trauma_type_name):
    """Get modern solutions for a specific trauma type"""
    try:
        trauma_type = TraumaType.objects.get(name=trauma_type_name)
        modern_content = ModernProgressContent.objects.filter(trauma_type=trauma_type)
        
        content_data = []
        for content in modern_content:
            content_data.append({
                'id': content.id,
                'title': content.title,
                'modern_solution': content.modern_solution,
                'therapy_type': content.therapy_type,
                'scientific_basis': content.scientific_basis,
                'resources': content.resources
            })
        
        return JsonResponse({'modern_content': content_data})
    
    except TraumaType.DoesNotExist:
        return JsonResponse({'error': 'Trauma type not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ============================================================================
# PROGRESS TRACKING
# ============================================================================

@csrf_exempt
def log_mood(request):
    """Log daily mood"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        mood_score = data.get('mood_score')
        note = data.get('note', '')
        
        user = User.objects.get(id=user_id)
        
        mood_log = MoodLog.objects.create(
            user=user,
            mood_score=mood_score,
            note=note
        )
        
        # Check for persistent low mood (trigger alert if needed)
        recent_logs = MoodLog.objects.filter(
            user=user,
            created_at__gte=timezone.now() - timedelta(days=7)
        ).order_by('-created_at')[:7]
        
        if len(recent_logs) >= 5:
            avg_mood = sum(log.mood_score for log in recent_logs) / len(recent_logs)
            if avg_mood < 2.5:  # Consistently low mood
                Alert.objects.create(
                    user=user,
                    alert_type='low_mood',
                    severity='warning',
                    message='Your mood has been consistently low for the past week. Consider reaching out to a mental health professional.'
                )
        
        return JsonResponse({
            'success': True,
            'mood_log': {
                'id': str(mood_log.id),
                'mood_score': mood_log.mood_score,
                'created_at': mood_log.created_at.isoformat()
            }
        })
    
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def get_mood_history(request):
    """Get mood history for a user"""
    try:
        user_id = request.GET.get('user_id')
        days = int(request.GET.get('days', 30))
        
        user = User.objects.get(id=user_id)
        
        mood_logs = MoodLog.objects.filter(
            user=user,
            created_at__gte=timezone.now() - timedelta(days=days)
        ).order_by('-created_at')
        
        logs_data = []
        for log in mood_logs:
            logs_data.append({
                'id': str(log.id),
                'mood_score': log.mood_score,
                'note': log.note,
                'created_at': log.created_at.isoformat()
            })
        
        return JsonResponse({'mood_logs': logs_data})
    
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def get_alerts(request):
    """Get active alerts for a user"""
    try:
        user_id = request.GET.get('user_id')
        user = User.objects.get(id=user_id)
        
        alerts = Alert.objects.filter(user=user, resolved=False).order_by('-triggered_at')
        
        alerts_data = []
        for alert in alerts:
            alerts_data.append({
                'id': str(alert.id),
                'alert_type': alert.alert_type,
                'severity': alert.severity,
                'message': alert.message,
                'triggered_at': alert.triggered_at.isoformat()
            })
        
        return JsonResponse({'alerts': alerts_data})
    
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ============================================================================
# GOVERNMENT SCHEMES
# ============================================================================

@csrf_exempt
def get_govt_schemes(request, trauma_type_name=None):
    """Get government schemes, optionally filtered by trauma type"""
    try:
        if trauma_type_name:
            trauma_type = TraumaType.objects.get(name=trauma_type_name)
            schemes = GovtScheme.objects.filter(trauma_type=trauma_type, is_active=True)
        else:
            schemes = GovtScheme.objects.filter(is_active=True)
        
        schemes_data = []
        for scheme in schemes:
            schemes_data.append({
                'id': scheme.id,
                'scheme_name': scheme.scheme_name,
                'description': scheme.description,
                'eligibility': scheme.eligibility,
                'link': scheme.link,
                'state': scheme.state,
                'trauma_type': scheme.trauma_type.name if scheme.trauma_type else None
            })
        
        return JsonResponse({'schemes': schemes_data})
    
    except TraumaType.DoesNotExist:
        return JsonResponse({'error': 'Trauma type not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
