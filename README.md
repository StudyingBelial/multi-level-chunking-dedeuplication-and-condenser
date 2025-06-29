# multi-level-semantic-chunking
This is a project associated with a research paper in order to provide practical evidence to support the findings.

## Table of Content
* [Project Overview](#project-overview)
* [Key Features](#key-features)
* [Setup, Installation and Dependencies](#setup-installation-and-dependencies)
* [Benchmark Guide](#benchmark-guide)
* [Associated Research Paper](#associated-research-paper)
* [License](#license)

## Project Overview
This project aims to create a multi-stages chunking process, to augment a preexisting technology of Semantic Chunking using Vector embeds. On a sentence by sentence level, Semantic Chunking is effective but costly, one of the ways to mitigate that is using a predefined window size to perfom the vector search on. This however creates an unintended issue where the window size may not be able to capture enough infomation that is semantically relavent, so we would need to employ larger and larger window sizes to get the information we need; there may even be a use case where having a defined window size is not perfect for the situation.

This is the problem that this project is attempting to solve, along with its research paper here. But the solution proposed here is to add an extra step before the semantic chunking process where we create large chunks of loosely related information which are achieved using Hierarchical clustering, without a set number of clusters but rather only based on a predefined distance threshold. This clustering algorithm creates large enough clusters that we can either run Semantic Chunking on without a window size on the entire chunk, and as the chunks are only a fraction of the size of the original document this saves on compute time. Or use very large window sizes where it is highly likely that the large window size will manage to capture all the required information as all the relavent is likely in the same chunk created by the clustering algorithm.

## Key Features
The main features of this entire repository discounting for all the setup and benchmarking are functions outlined below:
```
def clustering(sentences, sentence_embeddings, threshold_multiplier = 1)
def semantic_chunking(sentences, threshold_multiplier = 1)
def semantic_chunking_sliding_window(sentences, threshold_multiplier = 1, window_size = 15)
```
This is where the main solutions proposed are found. Do note that there are two semantic chunking functions one with a window size and one without a window size, this is done inorder to demonstrate that either of the two processes will yield better results from this system than a plain semantic chunking system.

The clustering function is doing all the clustering of the text data which is then used by either of the semantic chunking functions

## Setup, Installation and Dependencies
The only file needed to be run to verify the research is main.ipynb. The project folder does contain requirements.txt file but it is included in the prep work in the main.ipynb file, but creating a virtual environment before hand is recomended.
It is recomended that this environment contains a powerful GPU as the system is power hungry. The entire code was tested in Google Colabs free environment using the T4 GPU, as such the idea environment to run this repository is in Colab.

All the data used for the research will be automatically reproduced by the code but it does require a hugging face token for BBC and Textbook datasets, which are easy to obtain.

In the case that importing data failes please run these commands and try again:
```
pip install --upgrade datasets
```
```
pip install --upgrade faiss-cpu
```
```
pip install --upgrade faiss-gpu
```

## Benchmark Guide
There are a total of 4 benchmark scores measured by the system:
1. Aggregate Score using Cosine Similarity:
    This score measures the overall semantic similarity of the chunks calculated by the system, which is compared with the original chunks of the document.
    This score ranges from 0 to 1, where higher number indicates closer semantic meaning, while 0 means no similarity at all.

2. Adjusted Random Score (ARI):
    This score measures the similarity between two data clustering adjusted for chance. The output chunks are measured with the original chunks or reference chunk known as "ground truth".
    This score ranges from -1 to 1 where 1 indicates perfect agreement while 0 indicates agreement by random change and negative values suggest less agreement than even random chance.

3. Normalized Mutual Info Score (NMI):
    This score measures the mutual dependence between two clustering meaning it focuses on shared information, providing insight into how well the system captures the unerlying structure of the data defined by the ground truth.
    This score ranges from 0 to 1, where like ARI 1 indicates perfect alignment and 0 indicates no mutual information i.e clusters are independed of each other.

4. V Measure:
    This score is a harmonic mean of two other metrics of Homogenety and Completeness, for this system it is adjusted to prioritize Homogenety over Completeness which can be adjusted by changing the v_beta in
    ```
    def cluster_similarity(true_chunks, predicted_chunks, nmi_method = "geometric", v_beta = 0.85)
    ```
    where a v_beta closer to 1 represents Completeness and Homogenety having similar weight and a lower than 1 indicating Homogenety having more weight and higher than 1 representing Completeness having higher weight.
    This score also goes from 0 to 1 where 1 represents a perfect score after accounting for the v_beta.

## Associated Research Paper
**Title:** **Scalable Multi-Level Semantic Chunking for Condensation and Deduplication of Large-Scale Text Corpora via Hierarchical Clustering**
**Author:** **Aarya Bhandari** aka **StudyingBelial**
**Publication:** TO BE SEEN
**Abstract Summary:** Large Language Models (LLMs) have revolutionized text summarization and information extraction, yet their application for massive, multi-document and cataloguing remains computationally challenging, primarily dud to the exponential complexity presented by cross-document semantic comparison. This paper proposes a novel multi-stage text chunking methodology designed to overcome this scalability bottleneck. This approach first employs an agglomerative clustering algorithm to loosely group a large corpus of unprocessed text data into large, topically related macro-chunks. Subsequently, within each macro-chunk, distance-based semantic chunking is applied to identify atomic, semantically distinct units, effectively eliminating the need for computationally intensive global pairwise comparisons O (N²) where N is the total number of sentences and reducing it to a more efficient O (M * n²) where n is (N/M) and M is the number of macro-chunks. While this does not eliminate the exponential nature of the problem, the proposed solution turns the base into a fraction of the original. Experimental results on diverse large-scale text corpora demonstrates significant computational savings and improved efficiency in producing high-quality semantic chunks, making large scale text preprocessing for condensation and summarization practical.

## License
This project is licensed under the [MIT License](LICENSE)