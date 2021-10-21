from django.db import models
  
# Create your models here.
  
  
class React(models.Model):
    texte = models.TextField(blank = True)
    contexte = models.TextField(blank = True)

