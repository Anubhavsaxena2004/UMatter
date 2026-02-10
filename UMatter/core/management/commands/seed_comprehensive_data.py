"""
Django management command to seed comprehensive dummy data
Run with: python manage.py seed_comprehensive_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import (
    UserProfile, TraumaType, Question, UserAnswer, TraumaScore, DominantTrauma,
    RecoveryProgram, RecoveryStep, UserRecoveryProgress, Consultant, GovtScheme,
    HeritageContent, ModernProgressContent, MoodLog, Alert
)
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Seed database with comprehensive dummy data for UMatter (Ananya & Rahul)'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('='*70))
        self.stdout.write(self.style.WARNING('🌱 SEEDING COMPREHENSIVE DUMMY DATA'))
        self.stdout.write(self.style.WARNING('='*70))
        
        # Clear existing user-related data
        self.stdout.write('\n📦 Clearing existing user data...')
        UserAnswer.objects.all().delete()
        TraumaScore.objects.all().delete()
        DominantTrauma.objects.all().delete()
        UserRecoveryProgress.objects.all().delete()
        MoodLog.objects.all().delete()
        Alert.objects.all().delete()
        UserProfile.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        
        self.stdout.write(self.style.SUCCESS('✓ Cleared user data'))
        
        # 1️⃣ USERS & AUTH
        self.stdout.write('\n👤 Creating users and profiles...')
        
        # User 1: Ananya Sharma (Student, Delhi, 18-25)
        ananya = User.objects.create_user(
            username='ananya',
            email='ananya@gmail.com',
            password='password123',
            first_name='Ananya',
            last_name='Sharma'
        )
        UserProfile.objects.create(
            user=ananya,
            age_group='18-25',
            occupation='Student',
            location='Delhi',
            preferred_language='English'
        )
        self.stdout.write(f'  ✓ Created user: {ananya.username} (ananya@gmail.com)')
        
        # User 2: Rahul Verma (Software Engineer, Bengaluru, 26-35)
        rahul = User.objects.create_user(
            username='rahul',
            email='rahul@gmail.com',
            password='password123',
            first_name='Rahul',
            last_name='Verma'
        )
        UserProfile.objects.create(
            user=rahul,
            age_group='26-35',
            occupation='Software Engineer',
            location='Bengaluru',
            preferred_language='English'
        )
        self.stdout.write(f'  ✓ Created user: {rahul.username} (rahul@gmail.com)')
        
        # 2️⃣ TRAUMA ASSESSMENT MODULE
        self.stdout.write('\n🧠 Setting up trauma assessment data...')
        
        # Get trauma types (assuming they exist from seed_data.py)
        try:
            family = TraumaType.objects.get(name='Family')
            financial = TraumaType.objects.get(name='Financial')
            career = TraumaType.objects.get(name='Career')
            love = TraumaType.objects.get(name='Love')
            self.stdout.write('  ✓ Found 4 trauma types')
        except TraumaType.DoesNotExist:
            self.stdout.write(self.style.ERROR('  ✗ Trauma types not found. Please run: python manage.py seed_data first'))
            return
        
        # Get questions
        questions = Question.objects.all()
        if questions.count() < 5:
            self.stdout.write(self.style.ERROR('  ✗ Not enough questions. Please run: python manage.py seed_data first'))
            return
        
        # Get specific questions for answers
        q_financial_1 = questions.filter(trauma_type=financial).first()
        q_financial_2 = questions.filter(trauma_type=financial)[1] if questions.filter(trauma_type=financial).count() > 1 else None
        q_family_1 = questions.filter(trauma_type=family).first()
        q_career_1 = questions.filter(trauma_type=career).first()
        q_love_1 = questions.filter(trauma_type=love).first()
        
        # User Answers
        self.stdout.write('\n📝 Creating user answers...')
        
        # Ananya's answers (Financial stress dominant)
        if q_financial_1:
            UserAnswer.objects.create(user=ananya, question=q_financial_1, answer_value='D')  # Strongly Agree
        if q_financial_2:
            UserAnswer.objects.create(user=ananya, question=q_financial_2, answer_value='B')  # Disagree
        if q_family_1:
            UserAnswer.objects.create(user=ananya, question=q_family_1, answer_value='D')  # Strongly Agree
        
        self.stdout.write(f'  ✓ Created {UserAnswer.objects.filter(user=ananya).count()} answers for Ananya')
        
        # Rahul's answers (Career stress dominant)
        if q_career_1:
            UserAnswer.objects.create(user=rahul, question=q_career_1, answer_value='D')  # Strongly Agree
        if q_financial_2:
            UserAnswer.objects.create(user=rahul, question=q_financial_2, answer_value='B')  # Disagree
        
        self.stdout.write(f'  ✓ Created {UserAnswer.objects.filter(user=rahul).count()} answers for Rahul')
        
        # 3️⃣ TRAUMA CALCULATION / ML OUTPUT
        self.stdout.write('\n🤖 Creating trauma scores and dominant trauma...')
        
        # Ananya's scores
        TraumaScore.objects.create(
            user=ananya,
            trauma_type=financial,
            score_percentage=72.0,
            severity_level='high'
        )
        TraumaScore.objects.create(
            user=ananya,
            trauma_type=family,
            score_percentage=38.0,
            severity_level='moderate'
        )
        
        # Rahul's scores
        TraumaScore.objects.create(
            user=rahul,
            trauma_type=career,
            score_percentage=68.0,
            severity_level='high'
        )
        
        self.stdout.write(f'  ✓ Created {TraumaScore.objects.count()} trauma scores')
        
        # Dominant Trauma
        DominantTrauma.objects.create(
            user=ananya,
            primary_trauma=financial,
            secondary_trauma=family,
            confidence_score=0.85
        )
        DominantTrauma.objects.create(
            user=rahul,
            primary_trauma=career,
            confidence_score=0.78
        )
        
        self.stdout.write(f'  ✓ Created {DominantTrauma.objects.count()} dominant trauma records')
        
        # 4️⃣ RECOVERY & GUIDANCE
        self.stdout.write('\n🌱 Setting up recovery programs and progress...')
        
        # Get recovery programs
        financial_program = RecoveryProgram.objects.filter(trauma_type=financial).first()
        career_program = RecoveryProgram.objects.filter(trauma_type=career).first()
        
        if financial_program and career_program:
            # Get recovery steps
            financial_steps = RecoveryStep.objects.filter(program=financial_program)[:3]
            career_steps = RecoveryStep.objects.filter(program=career_program)[:3]
            
            # Ananya's progress (completed first step)
            if financial_steps:
                UserRecoveryProgress.objects.create(
                    user=ananya,
                    step=financial_steps[0],
                    status='completed',
                    completed_at=timezone.now() - timedelta(days=1)
                )
                self.stdout.write(f'  ✓ Created recovery progress for Ananya')
            
            # Rahul's progress (not started)
            if career_steps:
                UserRecoveryProgress.objects.create(
                    user=rahul,
                    step=career_steps[0],
                    status='not_started'
                )
                self.stdout.write(f'  ✓ Created recovery progress for Rahul')
        else:
            self.stdout.write(self.style.WARNING('  ⚠ Recovery programs not found, skipping progress'))
        
        # 5️⃣ CONSULTATION & SCHEMES
        self.stdout.write('\n👩‍⚕️ Creating consultants and government schemes...')
        
        Consultant.objects.get_or_create(
            name='Dr. Meera Joshi',
            defaults={
                'specialization': 'counselor',
                'contact_info': 'info@therapy.org | +91-9876543210',
                'availability': 'Mon-Fri, 10 AM - 6 PM',
                'verified': True
            }
        )
        
        Consultant.objects.get_or_create(
            name='Mr. Aman Roy',
            defaults={
                'specialization': 'career_coach',
                'contact_info': 'career@help.org | +91-9876543211',
                'availability': 'Tue-Sat, 2 PM - 8 PM',
                'verified': True
            }
        )
        
        self.stdout.write(f'  ✓ Created {Consultant.objects.count()} consultants')
        
        GovtScheme.objects.get_or_create(
            scheme_name='PM Jan Dhan Yojana',
            defaults={
                'trauma_type': financial,
                'description': 'Financial inclusion support for all citizens',
                'eligibility': 'All Indian citizens',
                'link': 'https://pmjdy.gov.in/',
                'state': 'National',
                'is_active': True
            }
        )
        
        GovtScheme.objects.get_or_create(
            scheme_name='Skill India',
            defaults={
                'trauma_type': career,
                'description': 'Career upskilling and vocational training',
                'eligibility': 'Youth aged 15-45',
                'link': 'https://www.skillindia.gov.in/',
                'state': 'National',
                'is_active': True
            }
        )
        
        self.stdout.write(f'  ✓ Created/verified government schemes')
        
        # 6️⃣ VIRASAT → VIKAS CONTENT
        self.stdout.write('\n🏛️ Creating heritage and modern content...')
        
        heritage1, created = HeritageContent.objects.get_or_create(
            trauma_type=financial,
            title='Ancient Financial Discipline',
            defaults={
                'historical_context': 'Arthashastra by Kautilya emphasized wealth management and economic stability',
                'practice': 'Mindful spending, saving for future, avoiding debt',
                'relevance_today': 'Financial stability through disciplined money management'
            }
        )
        
        heritage2, created = HeritageContent.objects.get_or_create(
            trauma_type=family,
            title='Joint Family Support',
            defaults={
                'historical_context': 'Indian culture traditionally valued extended family living together',
                'practice': 'Emotional sharing, collective decision-making, mutual support',
                'relevance_today': 'Mental support through strong family bonds'
            }
        )
        
        ModernProgressContent.objects.get_or_create(
            trauma_type=financial,
            title='Financial Therapy and CBT',
            defaults={
                'heritage_content': heritage1,
                'modern_solution': 'Budgeting apps and financial planning tools combined with CBT',
                'therapy_type': 'cbt',
                'scientific_basis': 'Behavioral science shows structured budgeting reduces financial anxiety',
                'resources': 'YNAB app, Mint, financial therapy resources'
            }
        )
        
        ModernProgressContent.objects.get_or_create(
            trauma_type=family,
            title='Family Systems Therapy',
            defaults={
                'heritage_content': heritage2,
                'modern_solution': 'Family therapy and counseling sessions',
                'therapy_type': 'psychotherapy',
                'scientific_basis': 'Psychology research validates importance of family support in mental health',
                'resources': 'Family therapy centers, online counseling platforms'
            }
        )
        
        self.stdout.write(f'  ✓ Created heritage and modern content')
        
        # 7️⃣ PROGRESS & SAFETY
        self.stdout.write('\n📊 Creating mood logs and alerts...')
        
        # Ananya's mood logs
        MoodLog.objects.create(
            user=ananya,
            mood_score=3,
            note='Feeling anxious about upcoming expenses',
            created_at=timezone.now() - timedelta(days=5)
        )
        MoodLog.objects.create(
            user=ananya,
            mood_score=2,
            note='Worried about tuition fees',
            created_at=timezone.now() - timedelta(days=4)
        )
        MoodLog.objects.create(
            user=ananya,
            mood_score=3,
            note='Talked to family, feeling slightly better',
            created_at=timezone.now() - timedelta(days=3)
        )
        MoodLog.objects.create(
            user=ananya,
            mood_score=4,
            note='Better after budgeting session',
            created_at=timezone.now() - timedelta(days=1)
        )
        MoodLog.objects.create(
            user=ananya,
            mood_score=4,
            note='Feeling more in control',
            created_at=timezone.now()
        )
        
        # Rahul's mood logs
        MoodLog.objects.create(
            user=rahul,
            mood_score=2,
            note='Very tired from work deadlines',
            created_at=timezone.now() - timedelta(days=4)
        )
        MoodLog.objects.create(
            user=rahul,
            mood_score=2,
            note='Burnout feeling intense',
            created_at=timezone.now() - timedelta(days=3)
        )
        MoodLog.objects.create(
            user=rahul,
            mood_score=3,
            note='Took a break, feeling slightly better',
            created_at=timezone.now() - timedelta(days=1)
        )
        MoodLog.objects.create(
            user=rahul,
            mood_score=3,
            note='Trying to set boundaries at work',
            created_at=timezone.now()
        )
        
        self.stdout.write(f'  ✓ Created {MoodLog.objects.count()} mood logs')
        
        # Alerts
        Alert.objects.create(
            user=rahul,
            alert_type='low_mood',
            severity='critical',
            message='Burnout Risk Detected: Your mood has been consistently low for 3+ days. Consider taking a break and consulting a professional.'
        )
        
        self.stdout.write(f'  ✓ Created {Alert.objects.count()} alerts')
        
        # SUMMARY
        self.stdout.write('\n' + '='*70)
        self.stdout.write(self.style.SUCCESS('🎉 COMPREHENSIVE DATABASE SEEDING COMPLETE!'))
        self.stdout.write('='*70)
        self.stdout.write('\n📊 DATA SUMMARY:')
        self.stdout.write(f'  👥 Users: {User.objects.filter(is_superuser=False).count()}')
        self.stdout.write(f'  📝 User Answers: {UserAnswer.objects.count()}')
        self.stdout.write(f'  📊 Trauma Scores: {TraumaScore.objects.count()}')
        self.stdout.write(f'  🎯 Dominant Traumas: {DominantTrauma.objects.count()}')
        self.stdout.write(f'  ✅ Recovery Progress: {UserRecoveryProgress.objects.count()}')
        self.stdout.write(f'  👩‍⚕️ Consultants: {Consultant.objects.count()}')
        self.stdout.write(f'  🏛️ Government Schemes: {GovtScheme.objects.count()}')
        self.stdout.write(f'  😊 Mood Logs: {MoodLog.objects.count()}')
        self.stdout.write(f'  🚨 Alerts: {Alert.objects.count()}')
        
        self.stdout.write('\n💡 TEST CREDENTIALS:')
        self.stdout.write('  Username: ananya | Password: password123')
        self.stdout.write('  Username: rahul  | Password: password123')
        
        self.stdout.write('\n🔗 USER JOURNEY FLOW:')
        self.stdout.write('  1. Users answer assessment questions ✓')
        self.stdout.write('  2. System calculates trauma scores ✓')
        self.stdout.write('  3. Assigns personalized recovery plans ✓')
        self.stdout.write('  4. Tracks mood and progress ✓')
        self.stdout.write('  5. Provides heritage-based + modern guidance ✓')
        self.stdout.write('  6. Generates alerts for concerning patterns ✓')
        self.stdout.write('\n')
