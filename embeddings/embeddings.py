import numpy as np
import spacy

nlp = spacy.load("en_core_web_lg")


def is_nan_or_empty(str_a, str_b):
    return str_a == 'nan' or str_b == 'nan' or str_a.strip() == '' or str_b.strip() == ''


def equality_embedding(str_a, str_b):
    if is_nan_or_empty(str_a, str_b):
        return 0.0
    return 1.0 if str_a == str_b else 0.0


def jaccard_embedding(year_of_birth_a, year_of_birth_b, year_of_death_a, year_of_death_b):
    union = min(year_of_birth_a, year_of_birth_b, year_of_death_a, year_of_death_b) \
            + max(year_of_birth_a, year_of_birth_b, year_of_death_a, year_of_death_b)
    if year_of_birth_a < year_of_birth_b:
        intersection = max(min(year_of_death_a, year_of_death_b) - year_of_birth_b, 0)
    else:
        intersection = max(min(year_of_death_b, year_of_death_a) - year_of_birth_a, 0)
    return intersection/union


def word2vec_embedding(str_a, str_b):
    if is_nan_or_empty(str_a, str_b):
        return 0.0
    doc1 = nlp(str_a)
    doc2 = nlp(str_b)
    return doc1.similarity(doc2)


def word2vec_str_embedding(string):
    if isinstance(string, str) is False:
        print(string)
        return np.nan
    return nlp(string).vector_norm


def book_similarity(book_data, other_book_data):
    embedding = []
    # type embedding
    embedding.append(equality_embedding(book_data['Type'], other_book_data['Type']))
    # title embedding
    embedding.append(word2vec_embedding(book_data['Title'], other_book_data['Title']))
    # language embedding
    embedding.append(equality_embedding(book_data['Language'], other_book_data['Language']))
    # subject embedding
    embedding.append(word2vec_embedding(book_data['Subjects'], other_book_data['Subjects']))
    # LoCC embedding
    embedding.append(word2vec_embedding(book_data['LoCC'], other_book_data['LoCC']))
    return embedding


