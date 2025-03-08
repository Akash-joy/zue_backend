from django.shortcuts import render
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .models import TaskState, Task
from .serializers import TaskStateSerializer,TaskSerializer
from rest_framework.views import APIView

class TaskStateList(generics.ListAPIView):
    queryset = TaskState.objects.all()
    serializer_class = TaskStateSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        all_tasks = Task.objects.all()
        task_serializer = TaskSerializer(all_tasks, many=True)
        custom_response = {
            "work_status": response.data,
            "tasks": task_serializer.data
        }
        return Response(custom_response)

class TaskCreateView(APIView):
    def post(self, request):
        request.data['created_date'] = timezone.now().date() 
        request.data['work_status'] = TaskState.objects.get(id=1).id

        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TaskDeleteView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()  # Get the task by id
            self.perform_destroy(instance)  # Delete the task
            return Response(status=status.HTTP_204_NO_CONTENT)  # Return success response
        except Task.DoesNotExist:
            return Response(
                {"error": "Task not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

class TaskUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'pk'  # This is the default, but you can specify it explicitly

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)  # Allow partial updates
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)