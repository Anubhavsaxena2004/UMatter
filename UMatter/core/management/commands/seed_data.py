"""
Django management command to seed the database with initial data
Run with: python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from core.models import (
    TraumaType, Question, RecoveryProgram, RecoveryStep,
    HeritageContent, ModernProgressContent, GovtScheme
)


class Command(BaseCommand):
    help = 'Seeds the database with initial data for UMatter'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting database seeding...')
        
        # Seed Trauma Types
        self.seed_trauma_types()
        
        # Seed Questions
        self.seed_questions()
        
        # Seed Recovery Programs
        self.seed_recovery_programs()
        
        # Seed Heritage Content
        self.seed_heritage_content()
        
        # Seed Modern Content
        self.seed_modern_content()
        
        # Seed Government Schemes
        self.seed_govt_schemes()
        
        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))

    def seed_trauma_types(self):
        self.stdout.write('Seeding trauma types...')
        
        trauma_data = [
            {
                'name': 'Family',
                'description': 'Family trauma includes experiences of abuse, neglect, loss, or harmful circumstances within the family unit.',
                'icon': '👨‍👩‍👧‍👦',
                'color_code': '#FF9933'
            },
            {
                'name': 'Financial',
                'description': 'Financial trauma refers to emotional distress from chronic money-related stress, lack of resources, or financial abuse.',
                'icon': '💰',
                'color_code': '#00A896'
            },
            {
                'name': 'Career',
                'description': 'Career trauma (workplace PTSD) is an emotional response to negative workplace events like termination, bullying, or toxic environments.',
                'icon': '💼',
                'color_code': '#F4A261'
            },
            {
                'name': 'Love',
                'description': 'Relationship trauma occurs when fundamental needs for connection, safety, and trust are violated within relationships.',
                'icon': '❤️',
                'color_code': '#E63946'
            },
        ]
        
        for data in trauma_data:
            TraumaType.objects.get_or_create(name=data['name'], defaults=data)
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(trauma_data)} trauma types'))

    def seed_questions(self):
        self.stdout.write('Seeding questions...')
        
        # Get trauma types
        family = TraumaType.objects.get(name='Family')
        financial = TraumaType.objects.get(name='Financial')
        career = TraumaType.objects.get(name='Career')
        love = TraumaType.objects.get(name='Love')
        
        questions_data = [
            # Family Questions
            {'trauma_type': family, 'order': 1, 'question_text': 'How often do you feel emotionally supported by your family?', 'weight': 1.5, 'is_critical': True},
            {'trauma_type': family, 'order': 2, 'question_text': 'Do you feel safe expressing your feelings at home?', 'weight': 1.3},
            {'trauma_type': family, 'order': 3, 'question_text': 'How would you describe communication in your family?', 'weight': 1.2},
            {'trauma_type': family, 'order': 4, 'question_text': 'Do you experience conflict or tension with family members?', 'weight': 1.4},
            
            # Financial Questions
            {'trauma_type': financial, 'order': 1, 'question_text': 'How often do you worry about money?', 'weight': 1.6, 'is_critical': True},
            {'trauma_type': financial, 'order': 2, 'question_text': 'Do you feel you have control over your financial situation?', 'weight': 1.4},
            {'trauma_type': financial, 'order': 3, 'question_text': 'How stressed do you feel about paying bills or debts?', 'weight': 1.5},
            {'trauma_type': financial, 'order': 4, 'question_text': 'Do financial concerns affect your sleep or daily life?', 'weight': 1.3},
            
            # Career Questions
            {'trauma_type': career, 'order': 1, 'question_text': 'How satisfied are you with your current work situation?', 'weight': 1.4, 'is_critical': True},
            {'trauma_type': career, 'order': 2, 'question_text': 'Do you feel valued and respected at work?', 'weight': 1.5},
            {'trauma_type': career, 'order': 3, 'question_text': 'How often do you feel overwhelmed by work demands?', 'weight': 1.3},
            {'trauma_type': career, 'order': 4, 'question_text': 'Do you experience work-related anxiety or stress?', 'weight': 1.6},
            
            # Love/Relationship Questions
            {'trauma_type': love, 'order': 1, 'question_text': 'How secure do you feel in your romantic relationships?', 'weight': 1.5, 'is_critical': True},
            {'trauma_type': love, 'order': 2, 'question_text': 'Do you trust your partner/potential partners?', 'weight': 1.6},
            {'trauma_type': love, 'order': 3, 'question_text': 'How comfortable are you with emotional intimacy?', 'weight': 1.3},
            {'trauma_type': love, 'order': 4, 'question_text': 'Do past relationship experiences affect your current well-being?', 'weight': 1.4},
        ]
        
        for data in questions_data:
            Question.objects.get_or_create(
                trauma_type=data['trauma_type'],
                order=data['order'],
                defaults={
                    'question_text': data['question_text'],
                    'weight': data['weight'],
                    'is_critical': data.get('is_critical', False)
                }
            )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(questions_data)} questions'))

    def seed_recovery_programs(self):
        self.stdout.write('Seeding recovery programs...')
        
        family = TraumaType.objects.get(name='Family')
        financial = TraumaType.objects.get(name='Financial')
        career = TraumaType.objects.get(name='Career')
        love = TraumaType.objects.get(name='Love')
        
        programs_data = [
            {
                'trauma_type': family,
                'title': 'Family Healing Journey',
                'description': 'A 30-day program to heal from family trauma through boundary-setting, self-compassion, and building healthy support networks.',
                'duration_days': 30,
                'difficulty_level': 'beginner',
                'steps': [
                    {'day': 1, 'type': 'journaling', 'title': 'Understanding Your Family Story', 'content': 'Write about your family dynamics and how they have shaped you.', 'duration': 20},
                    {'day': 2, 'type': 'meditation', 'title': 'Self-Compassion Meditation', 'content': 'Practice loving-kindness meditation focused on self-forgiveness.', 'duration': 15},
                    {'day': 3, 'type': 'reading', 'title': 'Healthy Boundaries 101', 'content': 'Learn about setting and maintaining healthy emotional boundaries.', 'duration': 25},
                ]
            },
            {
                'trauma_type': financial,
                'title': 'Financial Wellness Path',
                'description': 'A 30-day program combining practical financial skills with emotional healing from money-related stress.',
                'duration_days': 30,
                'difficulty_level': 'beginner',
                'steps': [
                    {'day': 1, 'type': 'practice', 'title': 'Money Mindset Assessment', 'content': 'Reflect on your beliefs about money and identify limiting patterns.', 'duration': 20},
                    {'day': 2, 'type': 'practice', 'title': 'Create a Simple Budget', 'content': 'Track your income and expenses for one week using the 50/30/20 rule.', 'duration': 30},
                    {'day': 3, 'type': 'breathing', 'title': 'Financial Anxiety Release', 'content': 'Practice deep breathing exercises to manage money-related anxiety.', 'duration': 15},
                ]
            },
            {
                'trauma_type': career,
                'title': 'Career Recovery Program',
                'description': 'A 30-day program to heal from workplace trauma and rebuild professional confidence.',
                'duration_days': 30,
                'difficulty_level': 'intermediate',
                'steps': [
                    {'day': 1, 'type': 'journaling', 'title': 'Work-Life Reflection', 'content': 'Write about your ideal work-life balance and current reality.', 'duration': 20},
                    {'day': 2, 'type': 'practice', 'title': 'Boundary Setting at Work', 'content': 'Identify one boundary you need to set and practice communicating it.', 'duration': 25},
                    {'day': 3, 'type': 'meditation', 'title': 'Stress Release Meditation', 'content': 'Guided meditation for releasing work-related stress and tension.', 'duration': 15},
                ]
            },
            {
                'trauma_type': love,
                'title': 'Relationship Healing Journey',
                'description': 'A 30-day program to heal from relationship trauma and build capacity for healthy connections.',
                'duration_days': 30,
                'difficulty_level': 'intermediate',
                'steps': [
                    {'day': 1, 'type': 'journaling', 'title': 'Relationship Patterns', 'content': 'Explore your relationship history and identify recurring patterns.', 'duration': 25},
                    {'day': 2, 'type': 'meditation', 'title': 'Heart Healing Meditation', 'content': 'Guided meditation for healing emotional wounds from past relationships.', 'duration': 20},
                    {'day': 3, 'type': 'reading', 'title': 'Attachment Styles', 'content': 'Learn about attachment theory and identify your attachment style.', 'duration': 30},
                ]
            },
        ]
        
        for prog_data in programs_data:
            program, created = RecoveryProgram.objects.get_or_create(
                trauma_type=prog_data['trauma_type'],
                title=prog_data['title'],
                defaults={
                    'description': prog_data['description'],
                    'duration_days': prog_data['duration_days'],
                    'difficulty_level': prog_data['difficulty_level']
                }
            )
            
            if created:
                for step_data in prog_data['steps']:
                    RecoveryStep.objects.create(
                        program=program,
                        day_number=step_data['day'],
                        activity_type=step_data['type'],
                        title=step_data['title'],
                        content=step_data['content'],
                        estimated_duration_minutes=step_data['duration']
                    )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(programs_data)} recovery programs'))

    def seed_heritage_content(self):
        self.stdout.write('Seeding heritage content...')
        
        family = TraumaType.objects.get(name='Family')
        financial = TraumaType.objects.get(name='Financial')
        career = TraumaType.objects.get(name='Career')
        love = TraumaType.objects.get(name='Love')
        
        heritage_data = [
            {
                'trauma_type': family,
                'title': 'Joint Family System and Emotional Support',
                'historical_context': 'Traditional Indian joint families provided built-in emotional support systems where elders guided younger members through challenges.',
                'practice': 'Regular family gatherings, respect for elders, collective decision-making, and shared responsibilities.',
                'relevance_today': 'While family structures have changed, the principle of building strong support networks remains crucial for emotional well-being.',
                'source': 'Ancient Indian Family Systems'
            },
            {
                'trauma_type': financial,
                'title': 'Santosha (Contentment) and Simple Living',
                'historical_context': 'Ancient Indian philosophy emphasized Santosha (contentment) as one of the Niyamas in Yoga, teaching satisfaction with what one has.',
                'practice': 'Practice gratitude, distinguish between needs and wants, live within means, and find joy in non-material aspects of life.',
                'relevance_today': 'In our consumer-driven society, practicing contentment can reduce financial anxiety and promote mental peace.',
                'source': 'Patanjali Yoga Sutras'
            },
            {
                'trauma_type': career,
                'title': 'Karma Yoga - Work as Service',
                'historical_context': 'The Bhagavad Gita teaches Karma Yoga, the path of selfless action without attachment to results.',
                'practice': 'Focus on doing your best work without obsessing over outcomes, find meaning in service, and maintain work-life balance.',
                'relevance_today': 'This approach reduces work-related stress by shifting focus from results to the quality of effort and contribution.',
                'source': 'Bhagavad Gita'
            },
            {
                'trauma_type': love,
                'title': 'Maitri and Karuna (Loving-Kindness and Compassion)',
                'historical_context': 'Buddhist and Hindu traditions emphasize Maitri (loving-kindness) and Karuna (compassion) as foundations for all relationships.',
                'practice': 'Cultivate self-love first, practice empathy, communicate with kindness, and approach conflicts with compassion.',
                'relevance_today': 'These principles help build healthy, resilient relationships based on mutual respect and understanding.',
                'source': 'Buddhist and Hindu Traditions'
            },
        ]
        
        for data in heritage_data:
            HeritageContent.objects.get_or_create(
                trauma_type=data['trauma_type'],
                title=data['title'],
                defaults={
                    'historical_context': data['historical_context'],
                    'practice': data['practice'],
                    'relevance_today': data['relevance_today'],
                    'source': data['source']
                }
            )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(heritage_data)} heritage content items'))

    def seed_modern_content(self):
        self.stdout.write('Seeding modern content...')
        
        family = TraumaType.objects.get(name='Family')
        financial = TraumaType.objects.get(name='Financial')
        career = TraumaType.objects.get(name='Career')
        love = TraumaType.objects.get(name='Love')
        
        modern_data = [
            {
                'trauma_type': family,
                'title': 'Family Systems Therapy',
                'modern_solution': 'Evidence-based therapy that views the family as an emotional unit, helping members understand patterns and improve communication.',
                'therapy_type': 'psychotherapy',
                'scientific_basis': 'Research shows family therapy effectively treats trauma, improving family functioning and individual mental health outcomes.',
                'resources': 'AAMFT (American Association for Marriage and Family Therapy), Psychology Today therapist directory'
            },
            {
                'trauma_type': financial,
                'title': 'Financial Therapy and Behavioral Economics',
                'modern_solution': 'Combines financial planning with psychological counseling to address the emotional aspects of money management.',
                'therapy_type': 'cbt',
                'scientific_basis': 'Studies show that addressing both practical and emotional aspects of finances leads to better financial outcomes and reduced anxiety.',
                'resources': 'Financial Therapy Association, YNAB (You Need A Budget) app, Mint budgeting tool'
            },
            {
                'trauma_type': career,
                'title': 'Workplace PTSD Treatment',
                'modern_solution': 'Specialized therapy combining CBT, EMDR, and stress management techniques for workplace trauma recovery.',
                'therapy_type': 'cbt',
                'scientific_basis': 'Research demonstrates that trauma-focused therapies effectively reduce symptoms of workplace PTSD and improve professional functioning.',
                'resources': 'BetterHelp, Talkspace, workplace EAP (Employee Assistance Programs)'
            },
            {
                'trauma_type': love,
                'title': 'Attachment-Based Therapy',
                'modern_solution': 'Therapy focused on understanding and healing attachment wounds to build secure, healthy relationships.',
                'therapy_type': 'psychotherapy',
                'scientific_basis': 'Attachment theory research shows that understanding attachment patterns helps individuals form healthier relationships and heal from past trauma.',
                'resources': 'Attached (book by Amir Levine), Hold Me Tight (book by Sue Johnson), couples therapy'
            },
        ]
        
        for data in modern_data:
            ModernProgressContent.objects.get_or_create(
                trauma_type=data['trauma_type'],
                title=data['title'],
                defaults={
                    'modern_solution': data['modern_solution'],
                    'therapy_type': data['therapy_type'],
                    'scientific_basis': data['scientific_basis'],
                    'resources': data['resources']
                }
            )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(modern_data)} modern content items'))

    def seed_govt_schemes(self):
        self.stdout.write('Seeding government schemes...')
        
        family = TraumaType.objects.get(name='Family')
        financial = TraumaType.objects.get(name='Financial')
        
        schemes_data = [
            {
                'trauma_type': family,
                'scheme_name': 'Kiran Mental Health Helpline',
                'description': '24/7 toll-free mental health rehabilitation helpline providing support for mental health concerns including family issues.',
                'eligibility': 'Available to all citizens of India',
                'link': 'https://www.mohfw.gov.in/',
                'state': 'National'
            },
            {
                'trauma_type': financial,
                'scheme_name': 'Pradhan Mantri Jan Dhan Yojana (PMJDY)',
                'description': 'Financial inclusion program providing access to banking, credit, insurance, and pension facilities.',
                'eligibility': 'All Indian citizens without bank accounts',
                'link': 'https://pmjdy.gov.in/',
                'state': 'National'
            },
            {
                'trauma_type': financial,
                'scheme_name': 'Stand Up India Scheme',
                'description': 'Facilitates bank loans for setting up greenfield enterprises by SC/ST and women entrepreneurs.',
                'eligibility': 'SC/ST and women entrepreneurs',
                'link': 'https://www.standupmitra.in/',
                'state': 'National'
            },
            {
                'trauma_type': None,
                'scheme_name': 'Manodarpan Initiative',
                'description': 'Psychosocial support for mental health and emotional well-being of students.',
                'eligibility': 'Students across India',
                'link': 'https://www.mhrd.gov.in/manodarpan',
                'state': 'National'
            },
        ]
        
        for data in schemes_data:
            GovtScheme.objects.get_or_create(
                scheme_name=data['scheme_name'],
                defaults={
                    'trauma_type': data['trauma_type'],
                    'description': data['description'],
                    'eligibility': data['eligibility'],
                    'link': data['link'],
                    'state': data['state']
                }
            )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(schemes_data)} government schemes'))
