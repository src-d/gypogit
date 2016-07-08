from binascii import unhexlify
from six import text_type
import unittest

from gypogit.blame import Blame
from gypogit.commit import Commit
from gypogit.core import ObjectType
from gypogit.file import File
from gypogit.objects import Signature
from gypogit.tree import Tree
from gypogit import GoGitError
from tests.base import GypogitTest


class CommitTest(GypogitTest):
    CH = "0e1bc15f54d17c218c0c92a704fdf6a16db9cee2"
    
    def setUp(self):
        self.commit = self.repo.Commit(self.CH)
        self.assertIsInstance(self.commit, Commit) 

    def test_properties(self):
        self.assertIsInstance(self.commit.Author, Signature)
        self.assertIsInstance(self.commit.Committer, Signature)
        self.assertIsInstance(self.commit.Hash, bytes)
        self.assertEqual(self.commit.Hash, unhexlify(self.hash))
        self.assertIsInstance(self.commit.Message, text_type)
        self.assertEqual(self.commit.Message.strip(),
                         "Wrap more objects with CGo")

    def test_methods_without_args(self):
        self.assertEqual(self.commit.ID(), unhexlify(self.hash))
        self.assertEqual(self.commit.Type(), ObjectType.Commit)
        self.assertEqual(self.commit.String(),
                         """commit 0e1bc15f54d17c218c0c92a704fdf6a16db9cee2
Author: Vadim Markovtsev <vadim@sourced.tech>
Date:   2016-06-21 17:14:53 +0300 +0300
""")
        self.assertIsInstance(self.commit.Tree(), Tree)

    def test_references(self):
        refs = self.commit.References("cshared/README.md")
        self.assertIsInstance(refs, (list, tuple))
        self.assertGreaterEqual(len(refs), 2)
        flags = [False, False]
        other_hash = "5df15d6acc505ae581d9a62e384503fea006b678"
        for rc in refs:
            self.assertIsInstance(rc, Commit)
            if rc.Hash == unhexlify(self.hash):
                flags[0] = True
            elif rc.Hash == unhexlify(other_hash):
                flags[1] = True
        for i in range(2):
            self.assertTrue(flags[i])
        self.assertEqual(
            len(self.commit.References("cshared/NO_README.md")), 0)

    def test_blame(self):
        blame = self.commit.Blame("cshared/README.md")
        self.assertIsInstance(blame, Blame)

    def test_parents(self):
        parents = list(self.commit.Parents())
        self.assertEqual(len(parents), 1)
        self.assertIsInstance(parents[0], Commit)
        self.assertEqual(
            parents[0].Hash,
            unhexlify("5df15d6acc505ae581d9a62e384503fea006b678"))
        self.assertEqual(self.commit.NumParents(), 1)

    def test_file(self):
        file = self.commit.File("cshared/README.md")
        self.assertIsInstance(file, File)
        self.assertIsInstance(file.Name, text_type)
        self.assertEqual(file.Name, "cshared/README.md")
        with self.assertRaises(GoGitError):
            self.commit.File("cshared/NO_README.md")


if __name__ == "__main__":
    unittest.main()
