update: download.py merge.py
	./download.py && ./merge.py && jupyter nbconvert --to script plot.ipynb \
	&& python3 plot.py
