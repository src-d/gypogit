from six import python_2_unicode_compatible, PY2, PY3

from .go_object import GoObject
from .objects import Signature, ObjectType, Blob
from .commit import Commit
from .tree import Tree
from .core import Object, ObjectIter


@python_2_unicode_compatible
class Tag(GoObject):
    @classmethod
    def Decode(cls, obj):
        assert isinstance(obj, Object)
        return Tag(cls._checked(cls.lib.c_Tag_Decode(obj.handle)))

    @property
    def Hash(self):
        return self._bytes(self.lib.c_Tag_get_Hash(self.handle))

    @property
    def Name(self):
        return self._string(self.lib.c_Tag_get_Name(self.handle))

    @property
    def Tagger(self):
        return Signature(self.lib.c_Tag_get_Tagger(self.handle))

    @property
    def Message(self):
        return self._string(self.lib.c_Tag_get_Message(self.handle))

    @property
    def TargetType(self):
        return ObjectType(self.lib.c_Tag_get_TargetType(self.handle))

    @property
    def Target(self):
        return self._bytes(self.lib.c_Tag_get_Target(self.handle))

    def ID(self):
        return self.Hash

    def Type(self):
        return ObjectType(self.lib.c_Tag_Type(self.handle))

    def String(self):
        return self._string(self.lib.c_Tag_String(self.handle))

    def __str__(self):
        return self.String()

    def Commit(self):
        return Commit(self._checked(self.lib.c_Tag_Commit(self.handle)))

    def Tree(self):
        return Tree(self._checked(self.lib.c_Tag_Tree(self.handle)))

    def Blob(self):
        return Blob(self._checked(self.lib.c_Tag_Blob(self.handle)))

    def Object(self):
        return Object(self._checked(self.lib.c_Tag_Object(self.handle)))


class TagIter(GoObject):
    @classmethod
    def New(cls, repo, it):
        from .repository import Repository
        assert isinstance(repo, Repository)
        assert isinstance(it, ObjectIter)
        return TagIter(cls.lib.c_NewTagIter(repo.handle, it.handle))

    def __iter__(self):
        return self

    if PY3:
        def __next__(self):
            return self._next()

    if PY2:
        def next(self):
            return self._next()

    def _next(self):
        handle = self._checked(self.lib.c_TagIter_Next(self.handle))
        if handle == self.INVALID_HANDLE:
            raise StopIteration()
        return Tag(handle)

    def __call__(self):
        while True:
            handle = self._checked(self.lib.c_TagIter_Next(self.handle))
            if handle == self.INVALID_HANDLE:
                break
            yield Tag(handle)
