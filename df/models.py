from django.db import models

class Person(models.Model):
    email=models.EmailField()
    diff=models.PositiveSmallIntegerField(max_length=1)
