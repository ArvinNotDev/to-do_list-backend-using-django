from django.http import Http404
from django.shortcuts import render
from rest_framework import permissions
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import Task
from .serializers import TaskSerializer, CustomTokenObtainPairSerializer
from django.utils.translation import gettext_lazy as _


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



class TaskListView(APIView):
    """
    API to list all tasks or create a new task.
    """
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(user=request.user.id).order_by('due_date')
        
        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = 5
        paginated_tasks = paginator.paginate_queryset(tasks, request)
        
        serializer = TaskSerializer(paginated_tasks, many=True)
        
        # Return paginated response
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailView(APIView):
    """
    api to view, update, or delete a task.
    """
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self, pk):
        task = get_object_or_404(Task, pk=pk)
        return task

    def get(self, request, pk):
        task = self.get_object(pk)
        if task.user == request.user:
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise Http404("No Task matches the given query.")

    def put(self, request, pk):
        task = self.get_object(pk)
        if task.user == request.user:
            serializer = TaskSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        raise Http404("No Task matches the given query.")

    def delete(self, request, pk):
        task = self.get_object(pk)
        if task.user == request.user:
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise Http404("No Task matches the given query.")
