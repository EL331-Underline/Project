from dataset import DatasetManager
from searcher import Searcher, SearcherQuery
from consistency import Consistency
from typing import Literal


def entry_point() -> Literal["dataset", "searcher", "consistency", "exit"]:
    while True:
        cmd = input("select operation: ")
        cmd = cmd.split()
        if len(cmd) != 1:
            print("too long")
            continue
        if cmd[0] == "dataset":
            return "dataset"
        elif cmd[0] == "searcher":
            return "searcher"
        elif cmd[0] == "consistency":
            return "consistency"
        elif cmd[0] == "exit":
            return "exit"
        else:
            print("available operations: dataset, searcher, consistency, exit")


def dataset_entry():
    cmd = input("(dataset) enter path to database: ")
    cmd = cmd.split()
    m = DatasetManager(cmd[0])
    dataset_body(m)
    del m


def dataset_body(m: DatasetManager):
    while True:
        cmd = input("(dataset) select operation: ")
        cmd = cmd.split()
        if cmd[0] == "create":
            if len(cmd) == 2:
                m.create(cmd[1], None)
            elif len(cmd) == 3:
                m.create(cmd[1], cmd[2])
            else:
                print("invalid number of arguments")
        elif cmd[0] == "retrieve":
            if len(cmd) == 2:
                print(m.retrieve(cmd[1]))
            else:
                print("invalid number of arguments")
        elif cmd[0] == "retrieve-names":
            if len(cmd) == 1:
                print(m.retrieve_names())
            else:
                print("invalid number of arguments")
        elif cmd[0] == "update":
            if len(cmd) == 3:
                print(m.update(cmd[1], cmd[2]))
            else:
                print("invalid number of arguments")
        elif cmd[0] == "delete":
            if len(cmd) == 2:
                print(m.delete(cmd[1]))
            else:
                print("invalid number of arguments")
        elif cmd[0] == "exit":
            return
        else:
            print("available operations: ", end="")
            print("create, retrieve, retrieve-names, update, delete, exit")


def searcher_entry():
    cmd = input("(searcher) enter path to database: ")
    cmd = cmd.split()
    m = DatasetManager(cmd[0])
    searcher_body(m)
    del m


def searcher_body(m: Searcher):
    s = Searcher(m)
    while True:
        cmd = input("(searcher) select operation: ")
        cmd = cmd.split()
        if cmd[0] == "search":
            if len(cmd) != 3:
                print("invalid number of arguments")
                continue
            r = s.search(SearcherQuery(cmd[1], cmd[2]))
            r.show()
            while True:
                yn = input("(searcher) save result? (y/n): ")
                if yn == "y":
                    r.save(".")
                    break
                elif yn == "n":
                    break
                else:
                    print("entry y or n")
        elif cmd[0] == "exit":
            return
        else:
            print("available operations: ", end="")
            print("search, exit")


def consistency_body(m: DatasetManager):
    s = Consistency(m)
    while True:
        cmd = input("(consistency) select operation: ")
        cmd = cmd.split()
        if cmd[0] == "compare":
            if len(cmd) != 1:
                print("invalid number of arguments")
                continue
            r = s.compare()
            r.show()
            while True:
                yn = input("(consistency) save result? (y/n): ")
                if yn == "y":
                    r.save(".")
                    break
                elif yn == "n":
                    break
                else:
                    print("entry y or n")
        elif cmd[0] == "exit":
            return
        else:
            print("available operations: ", end="")
            print("compare, exit")


def consistency_entry():
    cmd = input("(consistency) enter path to database: ")
    cmd = cmd.split()
    m = DatasetManager(cmd[0])
    consistency_body(m)
    del m


def main():
    while True:
        preload = input("create dataset from dataset folder? (y/n): ")
        if preload == "y":
            name = input("enter database name: ")
            m = DatasetManager(name)
            m.create("../dataset/AnwarKhoirul_20.txt", "K01")
            m.create("../dataset/AokiToshiaki_4.txt", "K02")
            m.create("../dataset/AsanoFumihiko_1.txt", "K03")
            m.create("../dataset/ChenJiageng_6.txt", "K04")
            m.create("../dataset/CheongKaiYuen_1.txt", "K05")
            m.create("../dataset/DangJiannwu_5.txt", "K06")
            m.create("../dataset/DefagoXavier_1.txt", "K07")
            m.create("../dataset/IkedaKokolo_2.txt", "K08")
            m.create("../dataset/InoguchiYasushi_1.txt", "K09")
            m.create("../dataset/MatsumotoTadashi_19.txt", "K10")
            m.create("../dataset/WirelessComm_unknown.txt", "Q")
            break
        elif preload == "n":
            break
        else:
            print("entry y or n")

    while True:
        operation = entry_point()
        if operation == "dataset":
            dataset_entry()
        elif operation == "searcher":
            searcher_entry()
        elif operation == "consistency":
            consistency_entry()
        else:
            return


if __name__ == "__main__":
    main()
