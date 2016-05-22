from django.db import models

nullable = {'blank': True, 'null': True}

class SourceLine(models.Model):

    project = models.CharField(max_length=200, **nullable)
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=20)
    line_number = models.IntegerField()
    kind = models.CharField(max_length=12)
    length = models.IntegerField()
    tags_json = models.CharField(max_length=1000, **nullable)

    def __unicode__(self):
        return '<{} {} {}:{}>'.format(
            self.__class__.__name__, self.name,
            self.path, self.line_number)

    @classmethod
    def projects(cls):
        projects = cls.objects.values('project').distinct(
        ).values_list('project', flat=True)
        return sorted(filter(None, projects))
