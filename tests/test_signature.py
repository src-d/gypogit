from datetime import datetime, date, timedelta
from six import text_type
import unittest

from gypogit.commit import Commit
from gypogit.objects import Signature
from tests.base import GypogitTest


class SignatureTest(GypogitTest):
    def test_properties(self):
        c = self.repo.Commit(self.hash)
        self.assertIsInstance(c, Commit)
        author = c.Author
        self.assertIsInstance(author, Signature)
        self.assertIsInstance(author.Name, text_type)
        self.assertEqual(author.Name, "Vadim Markovtsev")
        self.assertIsInstance(author.Email, text_type)
        self.assertEqual(author.Email, "vadim@sourced.tech")
        when = author.When
        self.assertIsInstance(when, datetime)
        self.assertEqual(when.date(), date(2016, 6, 21))
        self.assertEqual(when.hour, 17)
        self.assertEqual(when.minute, 14)
        self.assertEqual(when.tzinfo._offset, timedelta(0, 10800))


if __name__ == "__main__":
    unittest.main()
