from binascii import unhexlify
import unittest

from gypogit.core import ObjectType
from gypogit.file import File
from gypogit.tree import Tree
from tests.base import GypogitTest


class TreeTest(GypogitTest):
    TH = "322b85b8608a4b6de28c2cd14cf95e8a6795869c"

    def setUp(self):
        self.tree = self.repo.Tree(self.TH)
        self.assertIsInstance(self.tree, Tree)

    def test_properties(self):
        self.assertEqual(self.tree.Hash, unhexlify(self.TH))
        self.assertEqual(self.tree.ID(), unhexlify(self.TH))
        self.assertEqual(self.tree.Type(), ObjectType.Tree)

    def test_entries(self):
        entries = list(self.tree.Entries)
        self.assertEqual(len(entries), 35)
        self.assertEqual(len(entries[0]), 3)
        entries = {e[0]: e[1:] for e in entries}
        self.assertEqual(entries[".travis.yml"][0], 33188)
        self.assertEqual(entries["utils"][0], 16384)

    def test_files(self):
        files = list(self.tree.Files())
        self.assertEqual(len(files), 89)
        for f in files:
            self.assertIsInstance(f, File)

    def test_file(self):
        file = self.tree.File(".travis.yml")
        self.assertIsInstance(file, File)
        file = self.tree[".travis.yml"]
        self.assertIsInstance(file, File)
        self.assertEqual(file.Name, ".travis.yml")


if __name__ == "__main__":
    unittest.main()
