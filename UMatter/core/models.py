from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid


# ============================================================================
# MODULE 1: USER & AUTH
# ============================================================================

class UserProfile(models.Model):
    """Extended user profile information"""
    AGE_GROUPS = [
        ('18-25', '18-25 years'),
        ('26-35', '26-35 years'),
        ('36-45', '36-45 years'),
        ('46-60', '46-60 years'),
        ('60+', '60+ years'),
    ]
    
    LANGUAGES = [
        ('en', 'English'),
        ('hi', 'Hindi'),
        ('mr', 'Marathi'),
        ('ta', 'Tamil'),
        ('te', 'Telugu'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age_group = models.CharField(max_length=10, choices=AGE_GROUPS, null=True, blank=True)
    occupation = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    preferred_language = models.CharField(max_length=5, choices=LANGUAGES, default='en')
    phone = models.CharField(max_length=15, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


# ============================================================================
# MODULE 2: TRAUMA ASSESSMENT
# ============================================================================

class TraumaType(models.Model):
    """Static reference table for trauma categories"""
    TRAUMA_CHOICES = [
        ('Family', 'Family Trauma'),
        ('Financial', 'Financial Stress'),
        ('Career', 'Career Anxiety'),
        ('Love', 'Relationship Trauma'),
    ]
    
    name = models.CharField(max_length=50, choices=TRAUMA_CHOICES, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='❤️')
    color_code = models.CharField(max_length=7, default='#FF9933')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.get_name_display()
    
    class Meta:
        verbose_name = 'Trauma Type'
        verbose_name_plural = 'Trauma Types'
        ordering = ['name']


class Question(models.Model):
    """Assessment questions for trauma evaluation"""
    trauma_type = models.ForeignKey(TraumaType, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    weight = models.FloatField(
        default=1.0,
        validators=[MinValueValidator(0.1), MaxValueValidator(3.0)],
        help_text="Importance weight for this question (0.1 to 3.0)"
    )
    is_critical = models.BooleanField(
        default=False,
        help_text="Mark if this question is critical for assessment"
    )
    order = models.IntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.trauma_type.name} - Q{self.order}: {self.question_text[:50]}"
    
    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = ['trauma_type', 'order']
        unique_together = ['trauma_type', 'order']


class UserAnswer(models.Model):
    """Stores user responses to assessment questions"""
    ANSWER_CHOICES = [
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='user_answers')
    answer_value = models.CharField(max_length=1, choices=ANSWER_CHOICES)
    answered_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.question.trauma_type.name} - {self.answer_value}"
    
    class Meta:
        verbose_name = 'User Answer'
        verbose_name_plural = 'User Answers'
        ordering = ['-answered_at']
        unique_together = ['user', 'question']


# ============================================================================
# MODULE 3: ML CALCULATION ENGINE
# ============================================================================

class TraumaScore(models.Model):
    """Computed trauma scores for each user"""
    SEVERITY_LEVELS = [
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
        ('severe', 'Severe'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trauma_scores')
    trauma_type = models.ForeignKey(TraumaType, on_delete=models.CASCADE, related_name='scores')
    score_percentage = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    severity_level = models.CharField(max_length=10, choices=SEVERITY_LEVELS)
    calculated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.trauma_type.name}: {self.score_percentage:.1f}%"
    
    class Meta:
        verbose_name = 'Trauma Score'
        verbose_name_plural = 'Trauma Scores'
        ordering = ['-calculated_at']
        unique_together = ['user', 'trauma_type', 'calculated_at']


class DominantTrauma(models.Model):
    """Identifies primary and secondary trauma for each user"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dominant_trauma')
    primary_trauma = models.ForeignKey(
        TraumaType, 
        on_delete=models.CASCADE, 
        related_name='primary_for_users'
    )
    secondary_trauma = models.ForeignKey(
        TraumaType, 
        on_delete=models.CASCADE, 
        related_name='secondary_for_users',
        null=True,
        blank=True
    )
    confidence_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="ML confidence (0.0 to 1.0)"
    )
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - Primary: {self.primary_trauma.name}"
    
    class Meta:
        verbose_name = 'Dominant Trauma'
        verbose_name_plural = 'Dominant Traumas'


# ============================================================================
# MODULE 4: RECOVERY & GUIDANCE
# ============================================================================

class RecoveryProgram(models.Model):
    """Template recovery programs for each trauma type"""
    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    trauma_type = models.ForeignKey(TraumaType, on_delete=models.CASCADE, related_name='recovery_programs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration_days = models.IntegerField(default=30)
    difficulty_level = models.CharField(max_length=15, choices=DIFFICULTY_LEVELS, default='beginner')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.trauma_type.name} - {self.title}"
    
    class Meta:
        verbose_name = 'Recovery Program'
        verbose_name_plural = 'Recovery Programs'


class RecoveryStep(models.Model):
    """Individual activities within a recovery program"""
    ACTIVITY_TYPES = [
        ('meditation', 'Meditation'),
        ('exercise', 'Physical Exercise'),
        ('journaling', 'Journaling'),
        ('breathing', 'Breathing Exercise'),
        ('therapy', 'Therapy Session'),
        ('reading', 'Educational Reading'),
        ('practice', 'Practical Exercise'),
    ]
    
    program = models.ForeignKey(RecoveryProgram, on_delete=models.CASCADE, related_name='steps')
    day_number = models.IntegerField()
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    title = models.CharField(max_length=200)
    content = models.TextField()
    resources = models.TextField(blank=True, help_text="Links, videos, or additional resources")
    estimated_duration_minutes = models.IntegerField(default=15)
    
    def __str__(self):
        return f"Day {self.day_number}: {self.title}"
    
    class Meta:
        verbose_name = 'Recovery Step'
        verbose_name_plural = 'Recovery Steps'
        ordering = ['program', 'day_number']
        unique_together = ['program', 'day_number']


class UserRecoveryProgress(models.Model):
    """Tracks user completion of recovery steps"""
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('skipped', 'Skipped'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recovery_progress')
    step = models.ForeignKey(RecoveryStep, on_delete=models.CASCADE, related_name='user_progress')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='not_started')
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, help_text="User's personal notes")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.step.title}: {self.status}"
    
    class Meta:
        verbose_name = 'User Recovery Progress'
        verbose_name_plural = 'User Recovery Progress'
        unique_together = ['user', 'step']


# ============================================================================
# MODULE 5: CONSULTATION & SCHEMES
# ============================================================================

class Consultant(models.Model):
    """Mental health professionals and resources"""
    SPECIALIZATIONS = [
        ('clinical_psychologist', 'Clinical Psychologist'),
        ('counselor', 'Counselor'),
        ('psychiatrist', 'Psychiatrist'),
        ('therapist', 'Therapist'),
        ('social_worker', 'Social Worker'),
    ]
    
    name = models.CharField(max_length=200)
    specialization = models.CharField(max_length=30, choices=SPECIALIZATIONS)
    contact_info = models.TextField(help_text="Phone, email, or website")
    availability = models.CharField(max_length=200, blank=True)
    verified = models.BooleanField(default=False)
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_specialization_display()}"
    
    class Meta:
        verbose_name = 'Consultant'
        verbose_name_plural = 'Consultants'


class GovtScheme(models.Model):
    """Government support programs"""
    trauma_type = models.ForeignKey(
        TraumaType, 
        on_delete=models.CASCADE, 
        related_name='govt_schemes',
        null=True,
        blank=True
    )
    scheme_name = models.CharField(max_length=200)
    description = models.TextField()
    eligibility = models.TextField()
    link = models.URLField(max_length=500)
    state = models.CharField(max_length=50, blank=True, help_text="Specific to state, or 'National'")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.scheme_name
    
    class Meta:
        verbose_name = 'Government Scheme'
        verbose_name_plural = 'Government Schemes'


# ============================================================================
# MODULE 6: VIRASAT → VIKAS CONTENT (THEME)
# ============================================================================

class HeritageContent(models.Model):
    """Traditional Indian wisdom and practices"""
    trauma_type = models.ForeignKey(TraumaType, on_delete=models.CASCADE, related_name='heritage_content')
    title = models.CharField(max_length=200)
    historical_context = models.TextField(help_text="Historical background")
    practice = models.TextField(help_text="Traditional practice or wisdom")
    relevance_today = models.TextField(help_text="How it applies to modern life")
    source = models.CharField(max_length=200, blank=True, help_text="Source reference")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.trauma_type.name} - {self.title}"
    
    class Meta:
        verbose_name = 'Heritage Content'
        verbose_name_plural = 'Heritage Content'


class ModernProgressContent(models.Model):
    """Contemporary solutions and therapies"""
    THERAPY_TYPES = [
        ('cbt', 'Cognitive Behavioral Therapy'),
        ('mindfulness', 'Mindfulness-Based Therapy'),
        ('emdr', 'EMDR'),
        ('dbt', 'Dialectical Behavior Therapy'),
        ('psychotherapy', 'Psychotherapy'),
        ('group_therapy', 'Group Therapy'),
    ]
    
    heritage_content = models.ForeignKey(
        HeritageContent, 
        on_delete=models.CASCADE, 
        related_name='modern_solutions',
        null=True,
        blank=True
    )
    trauma_type = models.ForeignKey(TraumaType, on_delete=models.CASCADE, related_name='modern_content')
    title = models.CharField(max_length=200)
    modern_solution = models.TextField()
    therapy_type = models.CharField(max_length=20, choices=THERAPY_TYPES, blank=True)
    scientific_basis = models.TextField(help_text="Research or evidence supporting this")
    resources = models.TextField(blank=True, help_text="Books, apps, websites")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.trauma_type.name} - {self.title}"
    
    class Meta:
        verbose_name = 'Modern Progress Content'
        verbose_name_plural = 'Modern Progress Content'


# ============================================================================
# MODULE 7: PROGRESS & ANALYTICS
# ============================================================================

class MoodLog(models.Model):
    """Daily mood tracking"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mood_logs')
    mood_score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1=Very Bad, 5=Very Good"
    )
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.mood_score}/5 on {self.created_at.date()}"
    
    class Meta:
        verbose_name = 'Mood Log'
        verbose_name_plural = 'Mood Logs'
        ordering = ['-created_at']


class Alert(models.Model):
    """Crisis detection and alerts"""
    ALERT_TYPES = [
        ('low_mood', 'Persistent Low Mood'),
        ('crisis', 'Crisis Detected'),
        ('milestone', 'Milestone Achieved'),
        ('reminder', 'Activity Reminder'),
    ]
    
    SEVERITY_LEVELS = [
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    severity = models.CharField(max_length=10, choices=SEVERITY_LEVELS)
    message = models.TextField()
    triggered_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_alert_type_display()} ({self.severity})"
    
    class Meta:
        verbose_name = 'Alert'
        verbose_name_plural = 'Alerts'
        ordering = ['-triggered_at']
