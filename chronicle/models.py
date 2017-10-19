from django.db import models

# Create your models here.
class PokerSession(models.Model):
    text = models.TextField(default='')
    
