import numpy as np
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
        avg_processed_embed = np.mean(processed_embeddings, axis = 0)
    except Exception as e:
        print("An error occured while creating embeddings averages")
        print(e)

    try:
        similarity_score = cosine_similarity(np.array([avg_base_embed]), np.array([avg_processed_embed]))[0][0]
    except Exception as e:
        print("An error occured while calculating similarity score")
        print(e)

    return similarity_score

def cluster_similarity(true_chunks, predicted_chunks, nmi_method = "geometric", v_beta = 0.85):
    truth_sentences = {}
    true_sentence_extracted = 0
    for index, chunk in enumerate(true_chunks):
        for sentence in chunk:
            sentence = sentence.strip()
            if sentence:
                truth_sentences[sentence] = index
                true_sentence_extracted += 1

    predicted_sentences = {}
    predicted_sentences_extracted = 0
    for index, chunk in enumerate(predicted_chunks):
        for sentence in chunk:
            sentence = sentence.strip()
            if sentence:
                predicted_sentences[sentence] = index
                predicted_sentences_extracted += 1

    labels_true = []
    labels_pred = []
    sentence_matched_for_comparisoon = 0

    for sentence, id in predicted_sentences.items():
        if sentence in truth_sentences:
            labels_true.append(truth_sentences[sentence])
            labels_pred.append(id)
            sentence_matched_for_comparisoon += 1

    similarity_score = {}

    ari_score = adjusted_rand_score(labels_true, labels_pred)
    nmi_score = normalized_mutual_info_score(
        labels_true, 
        labels_pred, 
        average_method = nmi_method)
    v_measure = v_measure_score(
        labels_true, 
        labels_pred, 
        beta = v_beta)

    similarity_score["ari"] = ari_score
    similarity_score["nmi"] = nmi_score
    similarity_score["v_measure"] = v_measure

    return similarity_score