from crypt import methods
from email.policy import default

from django.core.serializers import serialize
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from task.models import Task
from task.serializers import TaskCreateSerializer, TaskSerializer


class TaskViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_completed', 'priority', 'due_date']
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'priority', 'created_at', 'title']

    def get_serializer_class(self):
        if self.action == 'create':
            return TaskCreateSerializer
        return TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)

        is_subtask = self.request.query_params.get('is_subtask')
        if is_subtask == 'false':
            queryset = queryset.filter(parent=None)
        elif is_subtask == 'true':
            queryset = queryset.exclude(parent=None)

        return queryset

    @action(detail=True, methods=['post'])
    def complete(self):
        task = self.get_object()
        task.is_completed = True
        task.completed_at = timezone.now()
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def uncomplete(self):
        task = self.get_object()
        task.is_completed = False
        task.completed_at = None
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

