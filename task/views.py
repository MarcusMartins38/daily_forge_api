from crypt import methods
from email.policy import default

from django.core.serializers import serialize
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
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
    ordering = ['-created_at']

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

    def perform_create(self, serializer):
        task = serializer.save(user=self.request.user)
        return task

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = self.perform_create(serializer)

        # Use TaskSerializer to get the complete response with subtasks
        response_serializer = TaskSerializer(task, context=self.get_serializer_context())
        headers = self.get_success_headers(serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        task = self.get_object()
        task.is_completed = True
        task.completed_at = timezone.now()
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def uncomplete(self, request, pk=None):
        task = self.get_object()
        task.is_completed = False
        task.completed_at = None
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def subtasks(self, request, pk=None):
        task = self.get_object()
        substask = task.subtasks.all()
        serializer = self.get_serializer(substask, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Obter tarefas atrasadas"""
        today = timezone.localdate()
        tasks = self.get_queryset().filter(
            due_date__date__lt=today,
            is_completed=False
        )
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)