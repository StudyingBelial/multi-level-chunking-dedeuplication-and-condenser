# multi-level-chunking-dedeuplication-and-condenser
This is a project associated with a research paper inorder to provide practical evidence to support the findings.

The only file needed to be run to verify the research is main.ipynb.
It is recomended that this environment contains a powerful GPU as the system is power intensive.
The test itself was done in the free environment of Google Colab using the T4 GPU.

In the case that import failes please use these commands:
```
pip install --upgrade datasets
```
```
pip install --upgrade faiss-cpu
```
```
pip install --upgrade faiss-gpu
```

All the data used for the research will be automatically reproduced by the code but it does require a hugging face token for BBC and Textbook datasets, which are easy to obtain.