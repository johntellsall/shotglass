# app/models.py

from colorfield.fields import ColorField
from django.db import models


nullable = {'blank': True, 'null': True}

class SourceFile(models.Model):
    project = models.CharField(max_length=200, **nullable)
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=200)
    language = models.CharField(max_length=12)
    num_lines = models.IntegerField()

    @classmethod
    def projects(cls):
        # pylint: disable=no-member
        projects = cls.objects.values(
            'project').distinct(
        ).order_by('project').values_list('project', flat=True)
        return list(projects)


class Symbol(models.Model):
    project = models.ForeignKey(SourceFile)
    label = models.CharField(max_length=200)
    line_number = models.IntegerField()
    # kind = models.CharField(max_length=12)
    # length = models.IntegerField()


# DEPRECATED:
class SourceLine(models.Model):

    project = models.CharField(max_length=200, **nullable)
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=200)
    line_number = models.IntegerField()
    kind = models.CharField(max_length=12)
    length = models.IntegerField()

    def __unicode__(self):
        return '<{} {} {}:{}>'.format(
            self.__class__.__name__, self.name,
            self.path, self.line_number)

    @classmethod
    def projects(cls):
        # pylint: disable=no-member
        projects = cls.objects.values(
            'project').distinct(
        ).values_list('project', flat=True)
        return sorted(filter(None, projects))

    @classmethod
    def paths(cls, project):
        # pylint: disable=no-member
        # X: sort?
        source = cls.objects.filter(project=project)
        return source.values('path').distinct().values_list(
            'path', flat=True)


class ProgRadon(models.Model):
    sourceline = models.OneToOneField(
        SourceLine, on_delete=models.CASCADE,
        **nullable)

    kind = models.CharField(max_length=1)
    complexity = models.IntegerField()


class ProgPmccabe(models.Model):
    sourceline = models.OneToOneField(
        SourceLine, on_delete=models.CASCADE,
        **nullable)

    modified_mccabe = models.IntegerField()
    mccabe = models.IntegerField()
    num_statements = models.IntegerField()
    first_line = models.IntegerField()
    num_lines = models.IntegerField()
    definition_line = models.IntegerField()


class Skeleton(models.Model):
    sourceline = models.ForeignKey(SourceLine, on_delete=models.CASCADE,
        **nullable)

    position = models.IntegerField()
    x = models.IntegerField()
    y = models.IntegerField()
    color = ColorField()
