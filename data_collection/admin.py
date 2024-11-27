from django.contrib import admin
from .models import PageVisit, QuizAttempt, Lesson, Profile

admin.site.register(PageVisit)
admin.site.register(QuizAttempt)
admin.site.register(Lesson)
admin.site.register(Profile)