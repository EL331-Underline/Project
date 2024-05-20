test_all: test_dataset test_searcher
	
test_dataset:
	python3 src/dataset.py

test_searcher:
	python3 src/searcher.py
