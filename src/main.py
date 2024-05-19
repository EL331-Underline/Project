from dataset import *
from searcher import *
def main():
    a = TestDatasetManager()
    a.test_create()
    a.test_retrieve()
    a.test_retrieve_names()
    a.test_update()
    a.test_delete()

if __name__ == "__main__":
    main()
