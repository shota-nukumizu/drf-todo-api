from rest_framework import serializers
from .models import Tag, Todo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    todo = TodoSerializer(many=True)

    class Meta:
        model = Tag
        fields = ['word']