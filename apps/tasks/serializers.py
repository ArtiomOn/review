from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Tasks


class TasksSerializer(ModelSerializer):

    class Meta:
        model = Tasks
        fields = ('id', 'title', 'description', 'assigned_to', 'created_by')
        extra_kwargs = {
            'created_by': {'read_only': True}
        }
