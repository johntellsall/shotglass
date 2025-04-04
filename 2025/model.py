from sqlmodel import Field, SQLModel


class SGGitHubRelease(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tag_name: str
    published_at: str
    gh_owner_repo: str

# Shotglass-specific fields prefixed with "sg_"

class SGAlpinePackage(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    alpine_release: str  # FIXME: rename -> sg_alpine_release
    pkgname: str
    pkgdesc: str
    pkgver: str
    pkgrel: str
    # sg_complexity: int | None = None
    # sg_len_build: int | None = None
    # sg_len_install: int | None = None
    # sg_len_subpackages: int | None = None
    sg_file_num_lines: int | None = None

    # FIXME: why?
    @classmethod
    def annotate(cls, data):
        return data

    # NOTE: move to 3rd library? vs parse or model
    # @classmethod
    # def annotate(cls, data):
    #     data = data.copy()
    #     def listlen(obj):
    #         if type(obj) is list:
    #             return len(obj)
    #         return 1
    #     # if data['pkgname'] == 'bash':
    #     #     breakpoint()
    #     data['sg_len_build'] = data['sg_len_install'] = 0
    #     try:
    #         data['sg_len_build'] = data['_parse_function_build']['length']
    #     except KeyError:
    #         pass
    #     try:
    #         data['sg_len_install'] = data['_parse_function_install']['length']
    #     except KeyError:
    #         pass
    #     data['sg_len_subpackages'] = listlen(data.get('subpackages', []))
    #     print('sg_len: ', data['sg_len_build'], data['sg_len_install'], data['sg_len_subpackages'])
    #     return data

#  '_parse_function_build': {'length': 17},
#  '_parse_function_package': {'length': 5},
#  '_parse_function_prepare': {'length': 12},

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
