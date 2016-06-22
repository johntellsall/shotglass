from colorfield.fields import ColorField
from django.db import models


nullable = {'blank': True, 'null': True}


# TODO: rename SourceLine to Symbol
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
        projects = cls.objects.values(  # pylint: disable=no-member
            'project').distinct(
        ).values_list('project', flat=True)
        return sorted(filter(None, projects))


class DiagramSymbol(models.Model):
    position = models.IntegerField()
    x = models.IntegerField()
    y = models.IntegerField()
    color = ColorField()
    sourceline = models.ForeignKey(SourceLine, on_delete=models.CASCADE,
        **nullable)


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
