from six import PY2, PY3, python_2_unicode_compatible

from .go_object import GoObject
from .core import ObjectIter, ObjectType
from .objects import Signature
from .tree import Tree
from .file import File
from .blame import Blame


@python_2_unicode_compatible
class Commit(GoObject):
    @classmethod
    def Decode(cls, obj):
        return Commit(cls._checked(cls.lib.c_Commit_Decode(obj.handle)))

    @property
    def Hash(self):
        return self._bytes(self.lib.c_Commit_get_Hash(self.handle), size=20)

    @property
    def Author(self):
        return Signature(self.lib.c_Commit_get_Author(self.handle))

    @property
    def Committer(self):
        return Signature(self.lib.c_Commit_get_Committer(self.handle))

    @property
    def Message(self):
        return self._string(self.lib.c_Commit_get_Message(self.handle))

    def Tree(self):
        return Tree(self.lib.c_Commit_Tree(self.handle))

    def Parents(self):
        return CommitIter(self.lib.c_Commit_Parents(self.handle))

    def NumParents(self):
        return self.lib.c_Commit_NumParents(self.handle)

    def File(self, path):
        return File(self._checked(self.lib.c_Commit_File(
            self.handle, self._string(path, self))))

    def ID(self):
        return self.Hash

    def Type(self):
        return ObjectType(self.lib.c_Commit_Type(self.handle))

    def String(self):
        return self._string(self.lib.c_Commit_String(self.handle))

    def __str__(self):
        return self.String()

    def References(self, path):
        rawrefs, size = self._checked(self.lib.c_Commit_References(
            self.handle, self._string(path, self)))
        refs = self.ffi.cast("uint64_t*", rawrefs)
        return [Commit(refs[i]) for i in range(size)]

    def Blame(self, path):
        return Blame(self._checked(self.lib.c_Commit_Blame(
            self.handle, self._string(path, self))))


class CommitIter(GoObject):
    @classmethod
    def New(cls, repo, it):
        from .repository import Repository
        assert isinstance(repo, Repository)
        assert isinstance(it, ObjectIter)
        return CommitIter(cls.lib.c_NewCommitIter(repo.handle, it.handle))

    def __iter__(self):
        return self

    if PY3:
        def __next__(self):
            return self._next()

    if PY2:
        def next(self):
            return self._next()

    def _next(self):
        handle = self._checked(self.lib.c_CommitIter_Next(self.handle))
        if handle == self.INVALID_HANDLE:
            raise StopIteration()
        return Commit(handle)

    def __call__(self):
        while True:
            handle = self._checked(self.lib.c_CommitIter_Next(self.handle))
            if handle == self.INVALID_HANDLE:
                break
            yield Commit(handle)
