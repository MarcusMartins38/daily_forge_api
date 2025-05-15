from django.db import models


class HabitLog(models.Model):
    habit = models.ForeignKey('habit.Habit', on_delete=models.CASCADE, related_name="logs")
    date = models.DateField()

    class Meta:
        unique_together = ('habit', 'date')

    def __str__(self):
        return f'{self.habit.name} - IsCompleted: {self.completed} - {self.date}'