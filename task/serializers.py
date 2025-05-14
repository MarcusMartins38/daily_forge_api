from rest_framework import serializers

from task.models import Task


class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'is_completed',
            'due_date', 'priority', 'created_at', 'updated_at', 'completed_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubtaskSerializer(many=True, read_only=True)
    is_subtask = serializers.BooleanField(read_only=True)
    has_subtasks = serializers.BooleanField(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'is_completed',
            'due_date', 'priority', 'parent', 'is_subtask',
            'has_subtasks', 'subtasks', 'created_at', 'updated_at',
            'completed_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'completed_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class TaskCreateSerializer(serializers.ModelSerializer):
    subtasks = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        write_only=True
    )

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'is_completed',
            'due_date', 'priority', 'parent', 'subtasks'
        ]

    def create(self, validated_data):
        subtasks_data = validated_data.pop('subtasks', [])
        user = self.context['request'].user
        validated_data['user'] = user

        task = super().create(validated_data)

        for subtask_data in subtasks_data:
            subtask_data['user'] = user
            subtask_data['parent'] = task
            Task.objects.create(**subtask_data)

        return task