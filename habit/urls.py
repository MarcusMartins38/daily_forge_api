from django.urls import path, include
from rest_framework.routers import DefaultRouter

from habit.views.habit import HabitViewSet
from habit.views.habit_log import ToggleHabitCompletion

router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habit')

urlpatterns = [
    path('', include(router.urls)),
    path('habits/<int:habit_id>/toggle/', ToggleHabitCompletion.as_view(), name='habit-toggle'),
]