import unittest
from gypogit import Repository


class GypogitTest(unittest.TestCase):
    URL = "https://github.com/src-d/go-git.git"

    @classmethod
    def setUpClass(cls):
        cls.repo = Repository.New(cls.URL)
        cls.repo.PullDefault()
