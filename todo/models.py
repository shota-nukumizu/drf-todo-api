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
    description = models.TextField(blank=True)
    priority = models.CharField(
        max_length=6,
        choices=PRIORITY_CHOICES
    )
    tags = models.ManyToManyField(Tag)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.title