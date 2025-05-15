from django.db import models
from django.utils import timezone

from habit.models.habit_log import HabitLog
from user.models import User


class Habit(models.Model):
    DAILY = 'day'
    WEEKLY = 'weekly'
    YEARLY = 'yearly'
    FREQUENCY_CHOICES = [
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly'),
        (YEARLY, 'Yearly')
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default=DAILY)
    start_date = models.DateTimeField(default=timezone.now())
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def mark_done(self, date=None):
        date = date or timezone.now().date()
        if not self.logs.filter(date=date).exists():
            HabitLog.objects.create(habit=self, date=date)

    def unmark_done(self, date=None):
        date = date or timezone.now().date()
        self.logs.filter(habit=self, date=date).delete()

    def is_done(self, date=None):
        date = date or timezone.now().date()
        return self.logs.filter(date=date).exists()

    def __str__(self):
        return self.name

