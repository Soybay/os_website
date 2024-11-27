from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()

class PageVisit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    path = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, null=True, blank=True)
    referer = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user} visited {self.path} at {self.timestamp}"

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz_name = models.CharField(max_length=255)
    score = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} attempted {self.quiz_name} on {self.timestamp}"

class Profile(models.Model):
    LEARNING_STYLES = [
        ('visual', 'Visual'),
        ('text', 'Text'),
        ('kinesthetic', 'Kinesthetic'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    learning_style = models.CharField(max_length=20, choices=LEARNING_STYLES, default='text')

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Lesson(models.Model):
    CONTENT_TYPES = [
        ('video', 'Video'),
        ('text', 'Text'),
        ('interactive', 'Interactive'),
    ]
    title = models.CharField(max_length=255)
    content = models.TextField()
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)

    def __str__(self):
        return self.title