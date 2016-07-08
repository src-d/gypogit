from six import PY2, PY3

from .go_object import GoObject
from .core import ObjectType


class File(GoObject):
    @property
    def Name(self):
        return self._string(self.lib.c_File_get_Name(self.handle))

    @property
    def Mode(self):
        return self.lib.c_File_get_Mode(self.handle)

    @property
    def Hash(self):
        return self._bytes(self.lib.c_File_get_Hash(self.handle), size=20)

    @property
    def Size(self):
        return self.lib.c_File_Size(self.handle)

    def ID(self):
        return self.Hash

    def Type(self):
        return ObjectType(self.lib.c_File_Type(self.handle))

    def Read(self):
        size, data = self._checked(self.lib.c_File_Read(self.handle), True)
        return self._bytes(data, size=size)

    def Contents(self, encoding="utf-8"):
        return self.Read().decode(encoding)

    def Lines(self):
        return list(iter(self))

    def __len__(self):
        return self.Size

    def __iter__(self):
        return iter(self.Contents().splitlines())


class FileIter(GoObject):
    @classmethod
    def New(cls, tree):
        return FileIter(cls.lib.c_NewFileIter(tree.handle))

    def __del__(self):
        if self.handle != self.INVALID_HANDLE:
            self.lib.c_FileIter_Close(self.handle)
        if GoObject is not None:
            GoObject.__del__(self)

    def __iter__(self):
        return self

    if PY3:
        def __next__(self):
            return self._next()

    if PY2:
        def next(self):
            return self._next()

    def _next(self):
        handle = self._checked(self.lib.c_FileIter_Next(self.handle))
        if handle == self.INVALID_HANDLE:
            raise StopIteration()
        return File(handle)

    def __call__(self):
        while True:
            handle = self._checked(self.lib.c_FileIter_Next(self.handle))
            if handle == self.INVALID_HANDLE:
                break
            yield File(handle)
