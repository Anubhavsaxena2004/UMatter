from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import UserProfile


def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            
            # Redirect to next page or home
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    
    return render(request, 'accounts/login.html')


def signup_view(request):
    """Handle user registration"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        
        # Profile data
        age_group = request.POST.get('age_group', '')
        occupation = request.POST.get('occupation', '')
        location = request.POST.get('location', '')
        preferred_language = request.POST.get('preferred_language', 'English')
        
        # Validation
        errors = []
        
        if not username or not email or not password1:
            errors.append('Username, email, and password are required.')
        
        if password1 != password2:
            errors.append('Passwords do not match.')
        
        if len(password1) < 8:
            errors.append('Password must be at least 8 characters long.')
        
        if User.objects.filter(username=username).exists():
            errors.append('Username already exists. Please choose another.')
        
        if User.objects.filter(email=email).exists():
            errors.append('Email already registered. Please use another or login.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'accounts/signup.html')
        
        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            
            # Create user profile
            UserProfile.objects.create(
                user=user,
                age_group=age_group if age_group else None,
                occupation=occupation if occupation else None,
                location=location if location else None,
                preferred_language=preferred_language
            )
            
            # Log the user in
            login(request, user)
            
            messages.success(request, f'Welcome to UMatter, {first_name or username}! Your healing journey begins now.')
            return redirect('home')
            
        except Exception as e:
            messages.error(request, f'An error occurred during registration: {str(e)}')
            return render(request, 'accounts/signup.html')
    
    return render(request, 'accounts/signup.html')


@login_required
def logout_view(request):
    """Handle user logout"""
    username = request.user.first_name or request.user.username
    logout(request)
    messages.success(request, f'Goodbye, {username}. Take care of yourself!')
    return redirect('home')


@login_required
def profile_view(request):
    """View and edit user profile"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        # Create profile if it doesn't exist
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        # Update profile
        profile.age_group = request.POST.get('age_group', profile.age_group)
        profile.occupation = request.POST.get('occupation', profile.occupation)
        profile.location = request.POST.get('location', profile.location)
        profile.preferred_language = request.POST.get('preferred_language', profile.preferred_language)
        profile.phone = request.POST.get('phone', profile.phone)
        profile.save()
        
        # Update user info
        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.last_name = request.POST.get('last_name', request.user.last_name)
        request.user.email = request.POST.get('email', request.user.email)
        request.user.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')
    
    context = {
        'profile': profile
    }
    return render(request, 'accounts/profile.html', context)
