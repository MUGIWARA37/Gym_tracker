from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from nutrition.models import NutritionGoal
from nutrition.serializers import NutritionGoalSerializer


class NutritionGoalView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        goal = NutritionGoal.objects.filter(user=request.user).first()
        if not goal:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(NutritionGoalSerializer(goal).data)

    def put(self, request):
        serializer = NutritionGoalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        NutritionGoal.objects.update_or_create(
            user=request.user, defaults=serializer.validated_data
        )
        goal = NutritionGoal.objects.get(user=request.user)
        return Response(NutritionGoalSerializer(goal).data, status=status.HTTP_201_CREATED)

    def patch(self, request):
        goal = NutritionGoal.objects.filter(user=request.user).first()
        if not goal:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = NutritionGoalSerializer(goal, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)
