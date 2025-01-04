from sqlmodel import Field, SQLModel, create_engine

# Shotglass-specific fields prefixed with "sg_"

class SGAlpinePackage(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    alpine_release: str  # FIXME: rename -> sg_alpine_release
    pkgname: str
    pkgdesc: str
    pkgver: str
    pkgrel: str
    sg_complexity: int | None = None
    sg_len_install: int | None = None
    sg_len_parse_funcs: int | None = None
    sg_len_subpackages: int | None = None

    # NOTE: move to 3rd library? vs parse or model
    @classmethod
    def annotate(cls, data):
        data = data.copy()
        def listlen(obj):
            if type(obj) is list:
                return len(obj)
            return 1
        data['sg_len_install'] = listlen(data.get('install', []))
        data['sg_len_parse_funcs'] = listlen(data.get('_parse_functions', []))
        data['sg_len_subpackages'] = listlen(data.get('subpackages', []))
        return data

# def setup():
#     sqlite_file_name = "database.db"
#     sqlite_url = f"sqlite:///{sqlite_file_name}"

#     engine = create_engine(sqlite_url, echo=True)

#     SQLModel.metadata.create_all(engine)