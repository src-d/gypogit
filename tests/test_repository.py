from six import text_type
import unittest

from gypogit import Remote
from gypogit.commit import Commit
from gypogit.core import ObjectStorage
from gypogit.objects import Blob
from gypogit.tag import Tag
from gypogit.tree import Tree
from tests.base import GypogitTest


class TestRepository(GypogitTest):
    def test_remotes(self):
        remotes = self.repo.Remotes
        self.assertEqual(len(remotes), 1)
        origin = remotes["origin"]
        self.assertIsInstance(origin, Remote)
        self.assertIsInstance(origin.Endpoint, text_type)
        self.assertEqual(origin.Endpoint, self.URL)

    def test_url(self):
        url = self.repo.Url
        self.assertIsInstance(url, text_type)
        self.assertEqual(url, self.URL)

    def test_storage(self):
        storage = self.repo.Storage
        self.assertIsInstance(storage, ObjectStorage)

    def test_commits(self):
        commits = list(self.repo.Commits())
        self.assertGreaterEqual(len(commits), 168)
        for c in commits:
            self.assertIsInstance(c, Commit)

    def test_pull(self):
        #self.repo.Pull("origin", "refs/heads/v2")
        pass

    def test_commit(self):
        c = self.repo.Commit("0e1bc15f54d17c218c0c92a704fdf6a16db9cee2")
        self.assertIsInstance(c, Commit)

    def test_tree(self):
        tree = self.repo.Tree("322b85b8608a4b6de28c2cd14cf95e8a6795869c")
        self.assertIsInstance(tree, Tree)

    def test_blob(self):
        blob = self.repo.Blob("388b676520a40064c6ead05f6d240a5003640e6a")
        self.assertIsInstance(blob, Blob)

    def test_tags(self):
        tags = list(self.repo.Tags())
        # self.assertGreaterEqual(len(tags), 10)
        # print(tags)
        for tag in tags:
            self.assertIsInstance(tag, Tag)

if __name__ == "__main__":
    unittest.main()
