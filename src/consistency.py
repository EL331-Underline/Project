import unittest
import dataset
import os
import datetime
import pathlib
import sys
from io import StringIO
from typing import Set, Dict, List
from dataset import DatasetManager
from tempfile import NamedTemporaryFile


class Table:
    """
    A class provide functionals to create tabular and show it.
    """

    def __init__(self):
        self.columns = []

    def add_column(self, tag: str, elements: List[str]):
        self.columns.append([tag, elements])

    def to_string(self) -> str:
        output = StringIO()

        row_len = 0
        columns_len = [0 for _ in range(len(self.columns))]
        for column in range(len(self.columns)):
            [tag, elements] = self.columns[column]
            row_len = max(row_len, len(elements))
            columns_len[column] = max(columns_len[column], len(tag))
            for element in elements:
                columns_len[column] = max(columns_len[column], len(element))

        for column in range(len(self.columns)):
            print("+" + "-" * (columns_len[column] + 2), end="", file=output)
        print("+", file=output)
        for column in range(len(self.columns)):
            tag = self.columns[column][0]
            spaces = " " * (columns_len[column] - len(tag))
            print("|" + " " + tag + spaces + " ", end="", file=output)
        print("|", file=output)
        for column in range(len(self.columns)):
            print("+" + "-" * (columns_len[column] + 2), end="", file=output)
        print("+", file=output)

        for row in range(row_len):
            for column in range(len(self.columns)):
                element = self.columns[column][1][row]
                spaces = " " * (columns_len[column] - len(element))
                print("|" + " " + element + spaces + " ", end="", file=output)
            print("|", file=output)

        for column in range(len(self.columns)):
            print("+" + "-" * (columns_len[column] + 2), end="", file=output)
        print("+", file=output)

        result = output.getvalue()
        output.close()
        return result


class ConsistencyResult:
    def __init__(
        self, number: int, words: List[str], names: List[str],
        words_by_name: Dict[str, Set[str]]
    ):
        """
        `words` and `names` must be sorted by correct way.
        """
        self.number = number
        self.words = words
        self.names = names
        self.words_by_name = words_by_name

    def show(self, output=sys.stdout):
        word_max_len = 0
        for word in self.words:
            word_max_len = max(word_max_len, len(word))

        table = Table()
        table.add_column("word", self.words)
        for name in self.names:
            column = []
            for word in self.words:
                if word in self.words_by_name[name]:
                    column.append("o")
                else:
                    column.append("x")
            table.add_column(name, column)
        print(table.to_string(), file=output)

    def save(self, path: str | os.PathLike):
        date = datetime.datetime.today().date()
        date = "{:04}{:02}{:02}".format(date.year, date.month, date.day)
        time = datetime.datetime.today().time()
        time = "{:02}{:02}".format(time.hour, time.minute)
        filename = "{:03}-{}-{}-consistency".format(
            self.number, date, time)
        path = pathlib.Path(path)
        if not path.is_dir():
            path.mkdir()
        path = path / filename
        with open(path, mode="w+") as f:
            self.show(f)


class Consistency:
    def __init__(self, manager: DatasetManager):
        self.counter = 0
        self.manager = manager

    def compare(self, qnames: List[str]) -> ConsistencyResult:
        names = sorted(qnames)
        words = set()
        words_by_name = dict()
        for name in names:
            words_by_name[name] = set()
        for name in names:
            for word in self.manager.retrieve(name).split():
                words.add(word)
                words_by_name[name].add(word)

        words_by_rank = [set() for _ in range(len(words) + 1)]
        for word in words:
            rank = 0
            for name in names:
                if word in words_by_name[name]:
                    rank += 1
            words_by_rank[rank].add(word)

        ordered_words = []
        for rank in reversed(range(len(words) + 1)):
            for word in sorted(words_by_rank[rank]):
                ordered_words.append(word)

        number = self.counter
        self.counter += 1
        return ConsistencyResult(number, ordered_words, names, words_by_name)


class TestConsistency(unittest.TestCase):
    def test_consistency(self):
        with NamedTemporaryFile(suffix="db") as db, \
                NamedTemporaryFile() as f1, \
                NamedTemporaryFile() as f2:
            with open(f1.name, "w+") as wf1:
                wf1.write("a b c d")
            with open(f2.name, "w+") as wf2:
                wf2.write("b c d e")

            m = dataset.DatasetManager(db.name)
            m.create(f1.name, "f1")
            m.create(f2.name, "f2")
            c = Consistency(m)
            r = c.compare(["f1", "f2"])
            self.assertEqual(r.names, ["f1", "f2"])
            self.assertEqual(r.words, ["b", "c", "d", "a", "e"])
            for w in ["a", "b", "c", "d"]:
                self.assertIn(w, r.words_by_name["f1"])
            for w in ["b", "c", "d", "e"]:
                self.assertIn(w, r.words_by_name["f2"])


if __name__ == "__main__":
    unittest.main()
