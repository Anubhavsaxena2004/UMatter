from django.contrib import admin
from .models import (
    UserProfile, TraumaType, Question, UserAnswer,
    TraumaScore, DominantTrauma, RecoveryProgram, RecoveryStep,
    UserRecoveryProgress, Consultant, GovtScheme, HeritageContent,
    ModernProgressContent, MoodLog, Alert
)


# ============================================================================
# USER & AUTH
# ============================================================================

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'age_group', 'occupation', 'location', 'preferred_language']
    list_filter = ['age_group', 'preferred_language']
    search_fields = ['user__username', 'user__email', 'occupation', 'location']
    readonly_fields = ['created_at', 'updated_at']


# ============================================================================
# TRAUMA ASSESSMENT
# ============================================================================

@admin.register(TraumaType)
class TraumaTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'color_code', 'created_at']
    search_fields = ['name', 'description']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['trauma_type', 'order', 'question_text_short', 'weight', 'is_critical']
    list_filter = ['trauma_type', 'is_critical']
    search_fields = ['question_text']
    ordering = ['trauma_type', 'order']
    
    def question_text_short(self, obj):
        return obj.question_text[:60] + '...' if len(obj.question_text) > 60 else obj.question_text
    question_text_short.short_description = 'Question'


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['user', 'question_trauma_type', 'answer_value', 'answered_at']
    list_filter = ['answer_value', 'answered_at']
    search_fields = ['user__username']
    readonly_fields = ['answered_at']
    
    def question_trauma_type(self, obj):
        return obj.question.trauma_type.name
    question_trauma_type.short_description = 'Trauma Type'


# ============================================================================
# ML CALCULATION ENGINE
# ============================================================================

@admin.register(TraumaScore)
class TraumaScoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'trauma_type', 'score_percentage', 'severity_level', 'calculated_at']
    list_filter = ['trauma_type', 'severity_level', 'calculated_at']
    search_fields = ['user__username']
    readonly_fields = ['calculated_at']


@admin.register(DominantTrauma)
class DominantTraumaAdmin(admin.ModelAdmin):
    list_display = ['user', 'primary_trauma', 'secondary_trauma', 'confidence_score', 'updated_at']
    list_filter = ['primary_trauma', 'secondary_trauma']
    search_fields = ['user__username']
    readonly_fields = ['updated_at']


# ============================================================================
# RECOVERY & GUIDANCE
# ============================================================================

@admin.register(RecoveryProgram)
class RecoveryProgramAdmin(admin.ModelAdmin):
    list_display = ['trauma_type', 'title', 'duration_days', 'difficulty_level', 'is_active']
    list_filter = ['trauma_type', 'difficulty_level', 'is_active']
    search_fields = ['title', 'description']


@admin.register(RecoveryStep)
class RecoveryStepAdmin(admin.ModelAdmin):
    list_display = ['program', 'day_number', 'activity_type', 'title', 'estimated_duration_minutes']
    list_filter = ['activity_type', 'program__trauma_type']
    search_fields = ['title', 'content']
    ordering = ['program', 'day_number']


@admin.register(UserRecoveryProgress)
class UserRecoveryProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'step_program', 'step_title', 'status', 'completed_at']
    list_filter = ['status', 'completed_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at']
    
    def step_program(self, obj):
        return obj.step.program.title
    step_program.short_description = 'Program'
    
    def step_title(self, obj):
        return obj.step.title
    step_title.short_description = 'Step'


# ============================================================================
# CONSULTATION & SCHEMES
# ============================================================================

@admin.register(Consultant)
class ConsultantAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization', 'location', 'verified']
    list_filter = ['specialization', 'verified']
    search_fields = ['name', 'location']


@admin.register(GovtScheme)
class GovtSchemeAdmin(admin.ModelAdmin):
    list_display = ['scheme_name', 'trauma_type', 'state', 'is_active']
    list_filter = ['trauma_type', 'state', 'is_active']
    search_fields = ['scheme_name', 'description']


# ============================================================================
# VIRASAT → VIKAS CONTENT
# ============================================================================

@admin.register(HeritageContent)
class HeritageContentAdmin(admin.ModelAdmin):
    list_display = ['trauma_type', 'title', 'source', 'created_at']
    list_filter = ['trauma_type']
    search_fields = ['title', 'practice']


@admin.register(ModernProgressContent)
class ModernProgressContentAdmin(admin.ModelAdmin):
    list_display = ['trauma_type', 'title', 'therapy_type', 'created_at']
    list_filter = ['trauma_type', 'therapy_type']
    search_fields = ['title', 'modern_solution']


# ============================================================================
# PROGRESS & ANALYTICS
# ============================================================================

@admin.register(MoodLog)
class MoodLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'mood_score', 'created_at', 'note_preview']
    list_filter = ['mood_score', 'created_at']
    search_fields = ['user__username', 'note']
    readonly_fields = ['created_at']
    
    def note_preview(self, obj):
        return obj.note[:50] + '...' if len(obj.note) > 50 else obj.note
    note_preview.short_description = 'Note'


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['user', 'alert_type', 'severity', 'triggered_at', 'resolved']
    list_filter = ['alert_type', 'severity', 'resolved', 'triggered_at']
    search_fields = ['user__username', 'message']
    readonly_fields = ['triggered_at']
