"""
URL configuration for UMatter project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('trauma-assessment/', TemplateView.as_view(template_name='trauma_assessment.html'), name='trauma_assessment'),
    path('selfcare/', TemplateView.as_view(template_name='selfcare_tips.html'), name='selfcare'),
    path('progress/', TemplateView.as_view(template_name='progress_tracker.html'), name='progress'),
    path('account/', TemplateView.as_view(template_name='account.html'), name='account'),
    path('api/', include('ScoringScoring.urls')),
    path('admin/', admin.site.urls),
]

