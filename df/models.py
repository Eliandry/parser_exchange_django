from django.db import models

class Person(models.Model):
    email=models.EmailField()
    time=models.TimeField()