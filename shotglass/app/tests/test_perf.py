import cProfile
import pstats
 
from django.test import TestCase

# PERFORMANCE TEST:
# py.test -s app/tests/test_perf::ProfileDraw
#
# TODO: disable this except when explicitly called
@pytest.mark.skip(reason="performance test only")
class ProfileDraw(TestCase):
    fixtures = ['diagram-django']  # slow + useful
    fixtures = ['diagram-min'] # minimal

    def setUp(self):
        stub = models.SourceLine.objects.create(
            kind='k', length=3, line_number=2, name='name', path='path')
        models.DiagramSymbol.objects.update(sourceline=stub)

    def test_rawdraw(self):
        def rawdraw():
            diagram = render.Diagram.FromDB()
            mygrid = grid.Grid(None, None)
            diagram.draw(mygrid)

        prof_name = 'rawdraw-{}.prof'.format(self.fixtures[0])
        cProfile.runctx(
            rawdraw.func_code,  # pylint: disable=no-member
            globals=globals(), locals={},
            filename=prof_name)

        p = pstats.Stats(prof_name)
        p.strip_dirs().sort_stats('cumtime').print_stats(20)

