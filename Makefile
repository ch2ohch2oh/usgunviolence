update: download_data.py merge_data.py
	./download_data.py && ./merge_data.py && ~/.local/bin/jupyter nbconvert --to script plot.ipynb \
	&& python3 plot.py
