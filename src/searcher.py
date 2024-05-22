import os
import dataset
import unittest


class SimpleSearcherQuery:
    pass


class SimpleSearcherResult:
    pass


class SimpleSearcher:
    """
    A class which provide a simple operations on specified dataset.
    """

    def __init__(self, database: str | os.PathLike):
        self.manager = dataset.DatasetManager(database)

    def __del__(self):
        del self.manager

    def search(self, query: SimpleSearcherQuery) -> SimpleSearcherResult:
        pass


class TestSimpleSearcher(unittest.TestCase):
    def test_search(self):
        pass


if __name__ == "__main__":
    unittest.main()
