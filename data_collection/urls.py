from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('quiz/', views.quiz_view, name='quiz'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('lessons/', views.lesson_view, name='lessons'),
    path('privacy/', views.privacy_policy_view, name='privacy_policy'),
    path('consent/', views.consent_view, name='consent'),
    path('signup/', views.signup_view, name='signup'),
]

