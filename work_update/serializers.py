from rest_framework import serializers
from .models import TaskState, Task

class TaskStateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskState
        fields = ['id', 'name']
        
    def get_tasks(self, obj):
        tasks = obj.task_set.all()  # Get all tasks associated with this state
        return TaskSerializer(tasks, many=True).data

class TaskSerializer(serializers.ModelSerializer):
    work_status = TaskStateSerializer(read_only=True)  # Nested representation
    class Meta: 
        model = Task
        fields = '__all__'  
    def update(self, instance, validated_data):
        # Handle the work_status field separately
        work_status_id = self.initial_data.get('work_status')
        if work_status_id:
            try:
                work_status = TaskState.objects.get(id=work_status_id)
                instance.work_status = work_status
            except TaskState.DoesNotExist:
                raise serializers.ValidationError({"work_status": "Invalid TaskState ID"})

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance