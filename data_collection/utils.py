# data_collection/utils.py

from .models import PageVisit, QuizAttempt
from django.db.models import Sum, Avg
import datetime


def infer_learning_style(user):
    visits = PageVisit.objects.filter(user=user)

    # Time spent on different content types
    visual_time = visits.filter(path__icontains='video').aggregate(total=Sum('duration'))[
                      'total'] or datetime.timedelta(0)
    text_time = visits.filter(path__icontains='text').aggregate(total=Sum('duration'))['total'] or datetime.timedelta(0)
    interactive_time = visits.filter(path__icontains='interactive').aggregate(total=Sum('duration'))[
                           'total'] or datetime.timedelta(0)

    # Average quiz scores for different content types (if applicable)
    # Assuming you have a way to link quiz attempts to content types
    # For simplicity, this example focuses on time spent

    # Determine learning style based on time spent
    times = {
        'visual': visual_time.total_seconds(),
        'text': text_time.total_seconds(),
        'kinesthetic': interactive_time.total_seconds(),
    }

    # Find the content type with the maximum time spent
    preferred_style = max(times, key=times.get)

    return preferred_style

# data_collection/utils.py
def calculate_score(answers):
    # Placeholder implementation
    # Replace this with your actual scoring logic
    return len(answers)