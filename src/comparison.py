import unittest
from typing import List, Tuple
from dataset import DatasetManager
from tempfile import NamedTemporaryFile


class ComparisonResult:
    def __init__(
        self,
        K_word: List[List[Tuple[str, int]]], Q_word: List[Tuple[str, int]]
    ):
        self.K_word = K_word
        self.Q_word = Q_word

    def show(self):
        K_word = [[] for i in range(len(self.K_word))]
        for i in range(len(self.K_word)):
            K_word[i] = sorted(
                self.K_word[i], key=lambda x: x[1], reverse=True)
        Q_word = sorted(self.Q_word, key=lambda x: x[1], reverse=True)
        K_max = 0
        for i in K_word:
            K_max = max(K_max, len(i))
        max_len = (max(K_max, len(Q_word)))
        for i in range(0, max_len, 20):
            print("Q ", end='')
            for j in range(i, i+20):
                if (j < len(Q_word)):
                    print(Q_word[j], end=' ')
            print()

            for max_len in range(len(K_word)):
                print("K"+str(max_len), end=' ')
                for j in range(i, i+20):
                    if (j < len(K_word)):
                        print(K_word[max_len][j], end=' ')
                print()


class Comparison:
    def __init__(self, manager: DatasetManager):
        self.manager = manager

    def compare(self, K_names: list[str], Q_name: str) -> ComparisonResult:
        K_size = len(K_names)
        K_res = [[] for i in range(K_size)]
        for i in range(K_size):
            K_text = self.manager.retrieve(K_names[i]).split()
            K_sum = {}
            for t in K_text:
                if (t in K_sum):
                    K_sum[t] += 1
                else:
                    K_sum[t] = 1
            for key, value in K_sum.items():
                K_res[i].append([key, value])
                # print(str(key) + ' ' + str(value))
            # print("end")

        Q_text = self.manager.retrieve(Q_name).split()
        Q_sum = {}
        for t in Q_text:
            if (t in Q_sum):
                Q_sum[t] += 1
            else:
                Q_sum[t] = 1

        Q_res = []
        for key, value in Q_sum.items():
            Q_res.append([key, value])

        return ComparisonResult(K_res, Q_res)


class Testcomparison(unittest.TestCase):
    def test_compmparison(self):

        with NamedTemporaryFile(suffix="db") as db, \
                NamedTemporaryFile() as f1, \
                NamedTemporaryFile() as f2, \
                NamedTemporaryFile() as f3:
            with open(f1.name, "w+") as wf1:
                wf1.write(
                    "bbb cccc aaa")

            with open(f2.name, "w+") as wf1:
                wf1.write(
                    "aaa aaa aaa aaa aaa")

            with open(f3.name, "w+") as wf1:
                wf1.write(
                    "ccc ccc aaa bbb aaa")
            m = DatasetManager(db.name)
            m.create(f1.name, "K1")
            m.create(f2.name, "Q")
            m.create(f3.name, "K2")

            c = Comparison(m)
            q = []
            q.append("K1")
            q.append("K2")
            res = c.compare(q, "Q")
            res.show()
            assert len(res.K_word[0]) == 3
            assert len(res.Q_word) == 1


if __name__ == "__main__":
    unittest.main()
