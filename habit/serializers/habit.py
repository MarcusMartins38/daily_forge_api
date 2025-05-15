from django.utils import timezone
from rest_framework import serializers

from habit.models.habit import Habit


class HabitSerializer(serializers.ModelSerializer):
    completed = serializers.SerializerMethodField()

    class Meta:
        model = Habit
        fields = ['id', 'name', 'description', 'start_date', 'frequency', 'is_active', 'completed', 'created_at', 'updated_at']
        read_only_fields = ['id', 'start_date']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def get_completed(self, obj):
        date = timezone.now().date()
        return obj.logs.filter(date=date).exists()