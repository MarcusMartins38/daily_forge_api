from rest_framework import serializers

from habit.models.habit_log import HabitLog


class HabitLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitLog
        fields = ['id', 'habit', 'date']
        read_only_fields = ['id']