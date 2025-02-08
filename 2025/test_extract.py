import extract
import pytest



def test_extract_apk_dir(mocker):
    topdir = 'aports/main/sqlite/'
    session = mocker.Mock()
    extract.extract_apk_dir(topdir, '1.23', session)
    session.add.assert_called_once()


def test_extract_apk_dir_error():
    topdir = 'BOGUS'
    with pytest.raises(ValueError):
        extract.extract_apk_dir(topdir, '1.23', None)