from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required 

from rest_framework import status

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

from .models import Todo
from .serializers import TodoSerializer

class TodoList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

class TodoDetail(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, todo_title, format=None):
        todo = Todo.objects.get(title=todo_title)
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

@method_decorator(login_required)
@api_view(['POST'])
def create(request):
    todo = TodoSerializer(data=request.data)

    if todo.is_valid():
        todo.save()
        return Response(todo.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@method_decorator(login_required)
@api_view(['POST'])
def update(request, pk):
    todo = Todo.objects.get(pk=pk)
    data = TodoSerializer(instance=todo, data=request.data)

    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@method_decorator(login_required)
@api_view(['DELETE'])
def delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.delete()
    return Response(status=status.HTTP_202_ACCEPTED)