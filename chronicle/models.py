from django.db import models

# Create your models here.
class Chronicles(models.Model):
    pass

class PokerSession(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(Chronicles, default=None)
