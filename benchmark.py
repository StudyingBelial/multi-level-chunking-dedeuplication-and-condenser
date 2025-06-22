import numpy as np
import spacy
from spacy.cli import download
from sklearn.metrics.pairwise import cosine_similarity, adjusted_rand_score, normalized_mutual_info_score, v_measure_score

def aggregate_similarity(base_embeddings, processed_embeddings):

    if base_embeddings is None or processed_embeddings is None:
        raise ValueError("No value passed for embeddings")

    base_embeddings = np.array(base_embeddings)
    processed_embeddings = np.array(processed_embeddings)


    if base_embeddings.size == 0:
        raise ValueError("Base embeddings is empty")

    if processed_embeddings.size == 0:
        raise ValueError("Processed Embeddings is empty")

    try:
        avg_base_embed = np.mean(base_embeddings, axis = 0)
        avg_preocessed_embed = np.mean(processed_embeddings, axis = 0)
    except Exception as e:
        print("An error occured while creating embeddings averages")
        print(e)

    try:
        similarity_score = cosine_similarity(np.array([avg_base_embed]), np.array([avg_preocessed_embed]))[0][0]
    except Exception as e:
        print("An error occured while calculating similarity score")
        print(e)

    return similarity_score

def cluster_similarity(true_chunks, predicted_chunks):
    # Download the spaCy small English model programmatically if not already installed
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")

    truth_sentences = []
    for index, chunk in enumerate(true_chunks):
        doc = nlp(chunk)
        for sentence in doc.sents:
            truth_sentences.append(
                {
                    "sentence" : sentence.text,
                    "chunk_id" : index
                }
            )

    predicted_sentences = []
    for index, chunk in enumerate(predicted_chunks):
        doc = nlp(chunk)
        for sentence in doc.sents:
            predicted_sentences.append({
                "sentence" : sentence.text,
                "chunk_id" : index
            })

    similarity_score = {}

    ari_score = adjusted_rand_score()
    nmi_score = normalized_mutual_info_score()
    v_measure = v_measure_score()

    similarity_score["ari"] = ari_score
    similarity_score["nmi"] = nmi_score
    similarity_score["v_measure"] = v_measure

    return similarity_score