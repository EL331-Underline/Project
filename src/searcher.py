import os
import dataset
import unittest
from typing import Literal


SearcherQueryKind = Literal["word token"]


SearcherQueryBody = str


class SearcherQuery:
    """
    A wrapper class to hold the kind of search and its body used for search.
    """

    def __init__(self, kind: SearcherQueryKind, body: SearcherQueryBody):
        self.kind = kind
        self.body = body


class SearcherResultElement:
    """
    One element the `SearcherResult` will holds.
    """

    def __init__(self, left: list[str], target: list[str], right: list[str]):
        self.left = left
        self.target = target
        self.right = right


class SearcherResult:
    """
    The result of search `Searcher.search` will returns.
    """

    def __init__(self, result: list[SearcherResultElement]):
        self.result = result

    def colorize(self):
        pass

    def save(self, path: str | os.PathLike):
        pass


class Searcher:
    """
    A class which provide a operation on specified dataset.
    """

    def __init__(self, database: str | os.PathLike):
        self.manager = dataset.DatasetManager(database)

    def __del__(self):
        del self.manager

    def search(self, query: SearcherQuery) -> SearcherResult:
        names = self.manager.retrieve_names()
        result = []
        for name in names:
            text = self.manager.retrieve(name).split()
            text_size = len(text)
            for j in range(text_size):
                if (text[j] == query.body):
                    left = []
                    mid = []
                    right = []
                    for k in range(max(0, j-11, j-1)):
                        left.append(text[k])

                    for k in range(j+1, min(j+11, text_size)):
                        right.append(text[k])

                    mid.append(text[j])
                    result.append(SearcherResultElement(left, mid, right))
        return SearcherResult(result)


class TestSearcher(unittest.TestCase):
    def test_search(self):
        pass


if __name__ == "__main__":
    unittest.main()
