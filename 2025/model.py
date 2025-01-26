from sqlmodel import Field, SQLModel

# Shotglass-specific fields prefixed with "sg_"

class SGAlpinePackage(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    alpine_release: str  # FIXME: rename -> sg_alpine_release
    pkgname: str
    pkgdesc: str
    pkgver: str
    pkgrel: str
    sg_complexity: int | None = None
    sg_len_build: int | None = None
    sg_len_install: int | None = None
    sg_len_subpackages: int | None = None

    # NOTE: move to 3rd library? vs parse or model
    @classmethod
    def annotate(cls, data):
        data = data.copy()
        def listlen(obj):
            if type(obj) is list:
                return len(obj)
            return 1
        data['sg_len_build'] = listlen(data.get('build', []))
        data['sg_len_install'] = listlen(data.get('install', []))
        # data['sg_len_parse_funcs'] = listlen(data.get('_parse_functions', []))
        data['sg_len_subpackages'] = listlen(data.get('subpackages', []))
        return data

# popcon ={'rank': 1, 'name': 'libacl1', 'inst': 138898, 'vote': 126117, 'old': 2, 'recent': 12764, 'no_files': 15,
# 'maintainer': 'Guillem Jover'}

class DebianPopContest(SQLModel, table=True):
    rank: int
    name: str | None = Field(default=None, primary_key=True)
    inst: int
    vote: int
    old: int
    recent: int
    no_files: int
    maintainer: str

# def setup():
#     sqlite_file_name = "database.db"
#     sqlite_url = f"sqlite:///{sqlite_file_name}"

#     engine = create_engine(sqlite_url, echo=True)

#     SQLModel.metadata.create_all(engine)