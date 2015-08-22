from django.db import models

nullable = {'blank': True, 'null': True}

class SourceLine(models.Model):
                    
    project = models.CharField(max_length=200, **nullable)
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=20)
    line_number = models.IntegerField()
    kind = models.CharField(max_length=12)
    length = models.IntegerField()
    
