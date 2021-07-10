# app/models.py

from colorfield.fields import ColorField
from django.db import models


nullable = {"blank": True, "null": True}


class SourceFile(models.Model):
    """
    file containing source code -- symbols
    """

    project = models.CharField(max_length=200, **nullable)
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=200)
    language = models.CharField(max_length=12)
    num_lines = models.IntegerField()

    # TODO: flesh out/remove
    @classmethod
    def projects(cls):
        # pylint: disable=no-member
        projects = (
            cls.objects.values("project")
            .distinct()
            .order_by("project")
            .values_list("project", flat=True)
        )
        return list(projects)


# {'kind': 'function', 'end': '384', 'language': 'Python',
# 'access': 'private', 'file': '', 'signature': '(x, y)',
# 'scope': 'function:TestRoutes.invoke.create_app', 'line': '383'}

# REPLACEMENT for SourceLine
class Symbol(models.Model):
    source_file = models.ForeignKey(SourceFile, on_delete=models.CASCADE)
    label = models.CharField(max_length=200)
    line_number = models.IntegerField()
    # kind = models.CharField(max_length=12)
    # length = models.IntegerField()

    def __repr__(self):
        cname = self.__class__.__name__
        return f"<{cname}: {self.label} line={self.line_number}>"


# DEPRECATED:
class SourceLine(models.Model):

    project = models.CharField(max_length=200, **nullable)
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=200)
    line_number = models.IntegerField()
    kind = models.CharField(max_length=12)
    length = models.IntegerField()

    def __unicode__(self):
        return "<{} {} {}:{}>".format(
            self.__class__.__name__, self.name, self.path, self.line_number
        )

    @classmethod
    def projects(cls):
        # pylint: disable=no-member
        projects = cls.objects.values("project").distinct()
        projects = projects.values_list("project", flat=True)
        return sorted(filter(None, projects))

    @classmethod
    def paths(cls, project):
        # pylint: disable=no-member
        # X: sort?
        source = cls.objects.filter(project=project)
        return source.values("path").distinct().values_list("path", flat=True)


# TODO: flesh out/remove
class ProgRadon(models.Model):
    sourceline = models.OneToOneField(
        SourceLine, on_delete=models.CASCADE, **nullable
    )  # noqa: E501

    kind = models.CharField(max_length=1)
    complexity = models.IntegerField()


# TODO: flesh out/remove
class ProgPmccabe(models.Model):
    sourceline = models.OneToOneField(
        SourceLine, on_delete=models.CASCADE, **nullable
    )  # noqa: E501

    modified_mccabe = models.IntegerField()
    mccabe = models.IntegerField()
    num_statements = models.IntegerField()
    first_line = models.IntegerField()
    num_lines = models.IntegerField()
    definition_line = models.IntegerField()


class Skeleton(models.Model):
    """
    rendering of a symbol: position and color
    """

    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, **nullable)

    position = models.IntegerField()
    x = models.IntegerField()
    y = models.IntegerField()
    color = ColorField()

    def __str__(self):
        cls_name = self.__class__.__name__
        return f"<{cls_name} pos={self.position} {self.color}>"
