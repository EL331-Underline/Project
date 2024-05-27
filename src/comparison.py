import unittest
import dataset
from io import StringIO
from typing import Set, Dict, List
from dataset import DatasetManager
from tempfile import NamedTemporaryFile

class ComparisonResult:
    def __init__(self,K_word: list[str,int], Q_word: list[str,int]):
        self.K_word = K_word;
        self.Q_word = Q_word;
    def show(self):
        K_word = sorted(self.K_word, key = lambda x:x[1], reverse = True)
        Q_word = sorted(self.Q_word, key = lambda x:x[1], reverse = True)

        l = (max(len(K_word),len(Q_word)))
        for i in range(0,l,20):
            print("K ",end = '')
            for j in range(i,i+20):
                if(j < len(K_word)):
                    print(K_word[j], end = ' ')
            print()
            print("Q ",end = '')
            for j in range(i,i+20):
                if(j < len(Q_word)):
                    print(Q_word[j],end = ' ')
            print()


class Comparison:
    def __init__(self,manager: DatasetManager):
        self.manager = manager
    
    def compare(self,K_name: str , Q_name: str) -> ComparisonResult:
        K_text = self.manager.retrieve(K_name).split()
        Q_text = self.manager.retrieve(Q_name).split()
        K_sum = {}
        Q_sum = {}
        
        for t in K_text:
            if(t in K_sum):
                K_sum[t] += 1
            else:
                K_sum[t] = 1;

        for t in Q_text:
            if(t in Q_sum):
                Q_sum[t] += 1
            else:
                Q_sum[t] = 1;
        
        K_res = []
        Q_res = []
        for key,value in K_sum.items():
            K_res.append([key,value])
        
        for key,value in Q_sum.items():
            Q_res.append([key,value])

        return ComparisonResult(K_res,Q_res)

class Testcomparison(unittest.TestCase):
    def test_compmparison(self):
        

        with NamedTemporaryFile(suffix="db") as db, NamedTemporaryFile() as f1,NamedTemporaryFile() as f2:
                with open(f1.name, "w+") as wf1:
                    wf1.write(
                        "bbb cccc")
                
                with open(f2.name, "w+") as wf1:
                    wf1.write(
                        "aaa aaa aaa aaa aaa")
                m = DatasetManager(db.name)
                m.create(f1.name,"K")
                m.create(f2.name,"Q")
                c = Comparison(m)
                res = c.compare("K","Q")
                res.show()
                assert len(res.K_word) == 2
                assert len(res.Q_word) == 1

if __name__ == "__main__":
        unittest.main()
 


