from binascii import unhexlify
from six import text_type
import unittest

from gypogit.core import ObjectType
from tests.base import GypogitTest


class TestFile(GypogitTest):
    TRAVIS_FILE = """language: go

go:
  - 1.4
  - 1.5
  - 1.6
  - tip

matrix:
  allow_failures:
    - go: tip

install:
  - rm -rf $GOPATH/src/gopkg.in/src-d
  - mkdir -p $GOPATH/src/gopkg.in/src-d
  - ln -s $PWD $GOPATH/src/gopkg.in/src-d/go-git.v3
  - go get -v -t ./...

script:
  - make test-coverage

after_success:
  - bash <(curl -s https://codecov.io/bash)
"""

    def setUp(self):
        self.file = self.repo.Tree(
            "322b85b8608a4b6de28c2cd14cf95e8a6795869c").File(".travis.yml")

    def test_properties(self):
        self.assertIsInstance(self.file.Name, text_type)
        self.assertEqual(self.file.Name, ".travis.yml")
        self.assertEqual(self.file.Mode, 33188)
        self.assertEqual(
            self.file.Hash,
            unhexlify("388b676520a40064c6ead05f6d240a5003640e6a"))
        self.assertEqual(self.file.Size, 346)
        self.assertEqual(self.file.ID(), self.file.Hash)
        self.assertEqual(self.file.Type(), ObjectType.Blob)

    def test_read(self):
        self.assertEqual(self.file.Read(), self.TRAVIS_FILE.encode())

    def test_contents(self):
        self.assertEqual(self.file.Contents(), self.TRAVIS_FILE)

    def test_lines(self):
        lines = self.file.Lines()
        self.assertIsInstance(lines, list)
        self.assertEqual(len(lines), 23)
        for line in lines:
            self.assertIsInstance(line, text_type)
        self.assertEqual("\n".join(lines) + "\n", self.TRAVIS_FILE)

    def test_iter(self):
        for line in self.file:
            self.assertIsInstance(line, text_type)


if __name__ == "__main__":
    unittest.main()
