from six import string_types, PY3, PY2

from .go_object import GoObject
from .core import Object, ObjectType
from .file import File, FileIter


class Tree(GoObject):
    @classmethod
    def Decode(cls, obj):
        assert isinstance(obj, Object)
        return Tree(cls._checked(cls.lib.c_Tree_Decode(obj.handle)))

    @property
    def Entries(self):
        size = self.lib.c_Tree_get_Entries_len(self.handle)
        for i in range(size):
            entry = self.lib.c_Tree_get_Entries_item(self.handle, i)
            cname, mode, chsh = entry.r0, entry.r1, entry.r2
            name = self._string(cname)
            hsh = self._bytes(chsh, size=20)
            yield name, mode, hsh

    @property
    def Hash(self):
        return self._bytes(self.lib.c_Tree_get_Hash(self.handle), size=20)

    def ID(self):
        return self.Hash

    def Type(self):
        return ObjectType(self.lib.c_Tree_Type(self.handle))

    def File(self, path):
        assert isinstance(path, string_types)
        return File(self._checked(self.lib.c_Tree_File(
            self.handle, self._string(path, self))))

    def __getitem__(self, item):
        return self.File(item)

    def Files(self):
        return FileIter(self.lib.c_Tree_Files(self.handle))
