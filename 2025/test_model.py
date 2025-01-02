from sqlmodel import create_engine, select, SQLModel, Session
from model import SGAlpinePackage
import pytest

ALPINE = {'_commit': '67c11662510f5e2db6e6517228e80b794950c43f',
 '_parse_functions': ['snapshot', 'package'],
 'arch': 'noarch',
 'builddir': '$srcdir/get-trust-anchor-$_commit',
 'license': 'Public-Domain',
 'makedepends': 'python3 openssl',
 'options': '"!check" # No tests',
 'pkgdesc': 'The DNSSEC root key(s)',
 'pkgname': 'dnssec-root',
 'pkgrel': '2',
 'pkgver': '20190225',
 'sha512sums': '"91b8fbecf10ae4d599a93bb69e342942a0f8dc3678c3ec8151dcdaa650eefdc4168eb5e272a4e4182daa180c3f5ff33217a825e2e8f19d489b6dc6171b0b5b56  '
               'dnssec-root-20190225.tar.gz',
 'source': '"$pkgname-$pkgver.tar.gz::https://github.com/iana-org/get-trust-anchor/archive/$_commit.tar.gz',
 'url': 'https://www.iana.org/dnssec/'}

ALPINE2 = {'_parse_functions': ['build', 'package'],
          'pkgdesc': 'A DNS traffic capture utility',
          'pkgname': 'dnstop',
          'pkgrel': '7',
          'pkgver': '20140915',
          'sha512sums': ['902cf96f7366983cae4bf684e44fbe12f6e982cee8ff489329e25e1a13de60870d356906a99fee56c6da2258c4a39074a504389549c6c2e239a4ea94d8b9a65d  '
                         'dnstop-20140915.tar.gz',
                         '8b1bcfb73f7acf8ab264f44a9fb3bb5bdc7b6beec3ea87ecf9d82898e83c5bd6e43bb12f6d72a9fe362c21210c4c2461c32bb23de03a938f20e2d7f0629f3a3d  '
                         'musl-fix.patch'],
          'source': '"http://dns.measurement-factory.com/tools/dnstop/src/dnstop-$pkgver.tar.gz',
          'subpackages': '$pkgname-doc',
          'url': 'http://dns.measurement-factory.com/tools/dnstop/'
          }


@pytest.fixture
def memdb():
    sqlite_url = "sqlite:///:memory:"
    engine = create_engine(sqlite_url) # FIXME: , echo=True)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_model(memdb):
    data = ALPINE.copy()
    data['sg_complexity'] = 123
    data['alpine_release'] = 'mytest'
    package = SGAlpinePackage(**data)
    memdb.add(package)
    memdb.commit()

    # select-exec style:
    statement = select(SGAlpinePackage).where(SGAlpinePackage.pkgname == "dnssec-root")
    results = memdb.exec(statement)
    result = results.one()
    assert result.pkgname == "dnssec-root"
    assert result.sg_complexity == 123


def test_annotate():
    data = ALPINE2.copy()
    data = SGAlpinePackage.annotate(data)
    assert data['sg_len_subpackages'] == 1


def test_annotate_db(memdb):
    data = SGAlpinePackage.annotate(ALPINE2)
    data['alpine_release'] = 'mytest'
    package = SGAlpinePackage(**data)
    memdb.add(package)
    memdb.commit()

    statement = select(SGAlpinePackage).where(SGAlpinePackage.pkgname == "dnstop")
    results = memdb.exec(statement)
    result = results.one()
    assert result.sg_len_subpackages == 1

