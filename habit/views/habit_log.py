from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from habit.models.habit import Habit


class ToggleHabitCompletion(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, habit_id):
        date = request.data.get("date", timezone.now().date())
        print(habit_id)
        habit = get_object_or_404(Habit, id=habit_id, user=request.user)

        if habit.is_done(date):
            habit.unmark_done(date)
            return Response({"status": "unmarked"})
        else:
            habit.mark_done(date)
            return Response({"status": "marked"})