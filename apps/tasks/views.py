from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Tasks
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    TasksSerializer,
    TasksListSerializer,
    TasksDetailSerializer,
    TasksUpdateAssignedUserSerializer,
    TasksUpdateStatusSerializer,
    TasksUpdateOwnerUserSerializer
)


# Create your views here.


class TasksListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Tasks.objects.all()
        serializer = TasksListSerializer(tasks, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=TasksSerializer)
    def post(self, request):
        serializer = TasksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)

            return HttpResponse(serializer.data['id'])
        return Response(serializer.errors)


class AllTasksDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Tasks.objects.get(pk=pk)
        except Tasks.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        instance = self.get_object(pk)
        serializer = TasksDetailSerializer(instance)
        return Response(serializer.data)

    def delete(self, request, pk):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status=status.HTTP_200_OK)


class UsersTasksDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Tasks.objects.filter(assigned_to=request.user)
        serializer = TasksListSerializer(tasks, many=True)
        return Response(serializer.data)


class CompletedTasksListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Tasks.objects.filter(status=True)
        serializer = TasksListSerializer(tasks, many=True)
        return Response(serializer.data)


class AssignTaskUserDetailView(APIView):
    def get_object(self, pk):
        try:
            return Tasks.objects.get(pk=pk)
        except Tasks.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=TasksUpdateAssignedUserSerializer)
    def patch(self, request, pk):
        instance = self.get_object(pk)
        serializer = TasksUpdateAssignedUserSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateTaskStatusDetailView(APIView):
    def get_object(self, pk):
        try:
            return Tasks.objects.get(pk=pk)
        except Tasks.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=TasksUpdateStatusSerializer)
    def patch(self, request, pk):
        instance = self.get_object(pk)
        serializer = TasksUpdateStatusSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssignTaskUserOwnerDetailView(APIView):
    def get_object(self, pk):
        try:
            return Tasks.objects.get(pk=pk)
        except Tasks.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=TasksUpdateOwnerUserSerializer)
    def patch(self, request, pk):
        instance = self.get_object(pk)
        serializer = TasksUpdateOwnerUserSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
