import spacy


def equality_embedding(str_a, str_b):
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
    nlp = spacy.load("en_core_web_lg")
    doc1 = nlp(str_a)
    doc2 = nlp(str_b)
    return doc1.similarity(doc2)

