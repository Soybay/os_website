from django.shortcuts import render, redirect, get_object_or_404
from .models import QuizAttempt, PageVisit, Profile, Lesson
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Sum
from .utils import infer_learning_style
import datetime
from django.contrib import messages
from .forms import ConsentForm


def calculate_score(answers):
    # Placeholder implementation
    return len(answers)  # Replace with your scoring logic

@login_required
def quiz_view(request):
    if request.method == 'POST':
        # Process quiz submission
        answers = request.POST.getlist('answers')
        score = calculate_score(answers)
        QuizAttempt.objects.create(
            user=request.user,
            quiz_name='Operating Systems Quiz 1',
            score=score
        )
        return redirect('quiz_results')
    else:
        # Render quiz page
        return render(request, 'data_collection/quiz.html')

@login_required
def analytics_view(request):
    # Total page visits per user
    page_visits = PageVisit.objects.filter(user=request.user).count()

    # Average quiz score
    average_score = QuizAttempt.objects.filter(user=request.user).aggregate(Avg('score'))['score__avg'] or 0

    # Most visited pages
    top_pages = PageVisit.objects.filter(user=request.user) \
                    .values('path') \
                    .annotate(visits=Count('id')) \
                    .order_by('-visits')[:5]

    # Time spent on site
    total_duration = PageVisit.objects.filter(user=request.user) \
                         .aggregate(total=Sum('duration'))['total'] or datetime.timedelta(0)

    # Infer learning style
    learning_style = infer_learning_style(request.user)

    # Update user's profile
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile.learning_style = learning_style
    profile.save()

    context = {
        'page_visits': page_visits,
        'average_score': average_score,
        'top_pages': top_pages,
        'total_duration': total_duration,
        'learning_style': learning_style,
    }
    return render(request, 'data_collection/analytics.html', context)

@login_required
def home_view(request):
    return render(request, 'data_collection/home.html')


@login_required
def lesson_view(request):
    # Get or create the user's profile
    profile, created = Profile.objects.get_or_create(user=request.user)
    learning_style = profile.learning_style

    content = Lesson.objects.filter(content_type=learning_style)

    if not content.exists():
        # If no content matches, provide all lessons or a default message
        messages.info(request, "No lessons available for your learning style. Showing all lessons.")
        content = Lesson.objects.all()
    # Fetch content based on learning style
    if learning_style == 'visual':
        content = Lesson.objects.filter(content_type='video')
    elif learning_style == 'text':
        content = Lesson.objects.filter(content_type='text')
    else:
        content = Lesson.objects.all()

    return render(request, 'data_collection/lesson.html', {'content': content})

def privacy_policy_view(request):
    return render(request, 'data_collection/privacy_policy.html')

def consent_view(request):
    if request.method == 'POST':
        form = ConsentForm(request.POST)
        if form.is_valid():
            # Mark that the user has given consent
            request.session['consent_given'] = True
            return redirect('home')
    else:
        form = ConsentForm()
    return render(request, 'data_collection/consent.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after signup
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'data_collection/signup.html', {'form': form})