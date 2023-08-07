import uuid

from django.db import models

# Create your models here.


class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False,
                            unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # This is an abstract class, so it won't be created in the database.
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Question(BaseModel):
    question = models.CharField(max_length=100)
    marks = models.IntegerField(default=5)
    category = models.ForeignKey(
        Category, related_name='category', on_delete=models.CASCADE)

    def __str__(self):
        return self.question


class Answer(BaseModel):
    answer = models.CharField(max_length=100)
    question = models.ForeignKey(
        Question, related_name='questions', on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer
