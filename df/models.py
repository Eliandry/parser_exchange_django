from django.db import models

class Person(models.Model):
    email=models.EmailField()
    time=models.TimeField()
class Corren(models.Model):
    doll = models.FloatField()
class Corren_euro(models.Model):
    euro = models.FloatField()