from django.urls import path
from . import views

urlpatterns = [
    # Assessment Flow
    path('questions/', views.get_questions_api, name='api_questions'),
    path('evaluate/', views.evaluate_assessment, name='api_evaluate'),
    
    # Recovery Plans
    path('recovery/plan/', views.get_recovery_plan, name='api_recovery_plan'),
    path('recovery/progress/', views.update_recovery_progress, name='api_recovery_progress'),
    
    # Heritage & Modern Content
    path('heritage/<str:trauma_type_name>/', views.get_heritage_content, name='api_heritage_content'),
    path('modern/<str:trauma_type_name>/', views.get_modern_content, name='api_modern_content'),
    
    # Progress Tracking
    path('mood/log/', views.log_mood, name='api_mood_log'),
    path('mood/history/', views.get_mood_history, name='api_mood_history'),
    path('alerts/', views.get_alerts, name='api_alerts'),
    
    # Government Schemes
    path('schemes/', views.get_govt_schemes, name='api_schemes_all'),
    path('schemes/<str:trauma_type_name>/', views.get_govt_schemes, name='api_schemes_by_trauma'),
]
