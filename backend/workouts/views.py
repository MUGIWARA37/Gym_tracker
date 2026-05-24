from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.permissions import IsOwner, IsOwnerOrCoach
from workouts.models import WorkoutPlan, WorkoutPlanExercise
from workouts.serializers import WorkoutPlanExerciseSerializer, WorkoutPlanSerializer


class WorkoutPlanViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutPlanSerializer
    search_fields = ["title", "description"]
    filterset_fields = ["goal", "difficulty", "is_public"]
    ordering_fields = ["created_at", "title"]

    def get_queryset(self):
        user = self.request.user
        return (
            WorkoutPlan.objects.filter(created_by=user)
            | WorkoutPlan.objects.filter(is_public=True)
        ).distinct()

    def get_permissions(self):
        if self.action in [
            "update",
            "partial_update",
            "exercises",
            "remove_exercise",
            "reorder_exercises",
        ]:
            return [IsOwnerOrCoach()]
        if self.action in ["destroy"]:
            return [IsOwner()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"])
    def duplicate(self, request, pk=None):
        original = self.get_object()
        new_plan = WorkoutPlan.objects.create(
            title=f"Copy of {original.title}",
            description=original.description,
            goal=original.goal,
            difficulty=original.difficulty,
            estimated_duration=original.estimated_duration,
            created_by=request.user,
            is_public=False,
        )
        for link in original.workoutplanexercise_set.all():
            WorkoutPlanExercise.objects.create(
                plan=new_plan,
                exercise=link.exercise,
                order=link.order,
                sets=link.sets,
                reps=link.reps,
                rest_time_seconds=link.rest_time_seconds,
            )
        return Response(WorkoutPlanSerializer(new_plan).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def exercises(self, request, pk=None):
        serializer = WorkoutPlanExerciseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(plan=self.get_object())
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["delete"], url_path="exercises/(?P<exercise_id>[^/.]+)")
    def remove_exercise(self, request, pk=None, exercise_id=None):
        link = WorkoutPlanExercise.objects.filter(
            plan_id=pk, exercise_id=exercise_id
        ).first()
        if not link:
            return Response(status=status.HTTP_404_NOT_FOUND)
        link.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["patch"], url_path="exercises/reorder")
    def reorder_exercises(self, request, pk=None):
        order_list = request.data.get("order", [])
        if not isinstance(order_list, list):
            return Response(
                {"detail": "Order must be a list of {id, order}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        for item in order_list:
            WorkoutPlanExercise.objects.filter(plan_id=pk, id=item.get("id")).update(
                order=item.get("order", 0)
            )
        return Response({"detail": "Order updated."})
