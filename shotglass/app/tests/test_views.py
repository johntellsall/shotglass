from pytest import mark

from app import views


class AttrDict(dict):
    __getattr__ = dict.__getitem__


# @mark.django_db
# def test_render():
# 	# just make sure it doesn't crash
# 	# X: depends on "flask" in database; add fixture
# 	views.render(None, project='flask')


# @mark.django_db
# def test_draw():
# 	# just make sure it doesn't crash
# 	req = AttrDict(GET={})
# 	views.draw(req, project='flask')
