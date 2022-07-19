from django.contrib import admin
from .models import Tag, Todo

admin.site.register(Todo)
admin.site.register(Tag)