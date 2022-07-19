# A simple Todo API Made in Django REST Framework

Django REST Frameworkで開発したシンプルなAPI。(Todoアプリ)

# 完成形

## `backend/settings.py`

```py
"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-dszy_!i)tz8jqfj(h%vnj88wdrj2%)njb6iw&o+&t1kd_&60co'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

CORS_ALLOW_ALL_ORIGINS = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'todo',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

## `backend/urls.py`

```py
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('todo.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
```

## `todo/models.py`

```py
from django.db import models

PRIORITY_CHOICES = [
    ('first', 'first'),
    ('second', 'second'),
    ('third', 'third'),
    ('fourth', 'fourth'),
]

class Tag(models.Model):
    word = models.CharField(max_length=40)

class Todo(models.Model):
    title = models.CharField(max_length=70)
    created = models.DateField(auto_now=True)
    description = models.TextField(blank=True)
    priority = models.CharField(
        max_length=6,
        choices=PRIORITY_CHOICES
    )
    tags = models.ManyToManyField(Tag)
    is_done = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.title
```

## `todo/serializers.py`

```py
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
```

## `todo/urls.py`

```py
from django.urls import path
from . import views

urlpatterns = [
    path('todos/', views.TodoList.as_view()),
    path('todos/<int:pk>', views.TodoDetail.as_view()),
    path('create/', views.create),
    path('update/<int:pk>', views.update),
    path('delete/<int:pk>', views.delete)
]
```

## `todo/views.py`

```py
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
```

# 開発環境

* Windows 11
* Django REST Framework
* Python