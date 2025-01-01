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

@pytest.fixture
def memdb():
    sqlite_url = "sqlite:///:memory:"
    engine = create_engine(sqlite_url, echo=True)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_model(memdb):
    package = SGAlpinePackage(**ALPINE)
    memdb.add(package)
    memdb.commit()

    # query style:
    if 0:
        result = memdb.query(SGAlpinePackage).filter(SGAlpinePackage.pkgname == "dnssec-root").first()
        assert result.pkgname == "dnssec-root"

    # select-exec style:
    statement = select(SGAlpinePackage).where(SGAlpinePackage.pkgname == "dnssec-root")
    results = memdb.exec(statement)
    result = results.one()
    assert result.pkgname == "dnssec-root"

    # SQL style:
    # result = memdb.exec(
    #     "SELECT * FROM sgalpinepackage WHERE pkgname = :pkgname",
    #     {"pkgname": "dnssec-root"}
    # ).first()
    # assert result.pkgname == "dnssec-root"