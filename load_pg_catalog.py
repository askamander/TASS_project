import pandas as pd
import numpy as np
import json
from tqdm import tqdm
from sklearn import preprocessing
import gower


from embeddings import book_similarity
from embeddings import word2vec_str_embedding
from find_knn import find_knn

DIR = 'data'


def one_hot_encode_pd_column(df, col_name):
    one_hot_type = pd.get_dummies(df[col_name])
    df = df.drop(col_name, axis=1)
    df = df.join(one_hot_type)
    return df


def load_and_preprocess_pg_catalog(path=f'{DIR}/pg_catalog.csv'):
    df = pd.read_csv(path)
    df = df.fillna('nan')
    df = df[["Type", "Title", "Language", "Subjects", "LoCC"]]
    df["Title"] = df["Title"].apply(lambda x: word2vec_str_embedding(x))
    min_max_scaler_titles = preprocessing.MinMaxScaler()
    titles_scaled = min_max_scaler_titles.fit_transform(np.array(df["Title"]).reshape(-1,1))
    df["Title"] = pd.DataFrame(titles_scaled.flatten())
    df["Subjects"] = df["Subjects"].apply(lambda x: word2vec_str_embedding(x))
    min_max_scaler_subjects = preprocessing.MinMaxScaler()
    subjects_scaled = min_max_scaler_subjects.fit_transform(np.array(df["Subjects"]).reshape(-1,1))
    df["Subjects"] = pd.DataFrame(subjects_scaled)
    # df = one_hot_encode_pd_column(df, 'Type')
    # df = one_hot_encode_pd_column(df, 'Language')
    # df = one_hot_encode_pd_column(df, 'LoCC')
    # df.to_csv(f'{DIR}/pg_catalog_to_cluster_one_hot.csv', index=False)
    return df


def load_pg_catalog_to_cluster(path=f'{DIR}/pg_catalog_to_cluster.csv'):
    df = pd.read_csv(path)
    return df


def load_preprocessed_pg_catalog(path=f'{DIR}/pg_catalog.csv'):
    df = pd.read_csv(path)
    df = df.fillna('nan')
    df.to_csv(f'{DIR}/pg_catalog_cleaned.csv', index=False)
    return df

if __name__ == '__main__':
    books_to_recommend_num = 50

    #
    #load_and_preprocess_pg_catalog()
    #

    df = load_pg_catalog_to_cluster()
    df_orig = load_preprocessed_pg_catalog()
    recommendations = {}
    for i in tqdm(range(len(df))):
        # print(df.iloc[i:i+1, :])
        topn = gower.gower_topn(df.iloc[i:i+1, :], df, n=books_to_recommend_num)
        recommendations[df_orig.iloc[i]['Title']] = {'books': df_orig.iloc[topn['index'][1:]]["Title"].tolist(),
                                                     'authors': df_orig.iloc[topn['index'][1:]]["Authors"].tolist(),
                                                     'addition_day': df_orig.iloc[topn['index'][1:]]["Issued"].tolist(),
                                                     'similarities': topn['values'].tolist()}

# print(recommendations)
# recommendations = {}
# for i in range(len(df)):
#     print(f'Book no. {i}')
#     embeddings = []
#     books = []
#     for j in tqdm(range(i+1, len(df), 1)):
#         embeddings.append(book_embedding(df.iloc[i], df.iloc[j]))
#         books.append(df.iloc[j]['Title'])
#         if j == 8:
#             break
#     indices = find_knn(books_to_recommend_num, embeddings, [[1 for _ in range(len(embeddings[0]))]])
#     recommendations[df.iloc[i]['Title']] = np.take(np.array(books), indices).flatten().tolist()
#     break
#
    json_recs = json.dumps(recommendations)
    with open('data/book_recommendations.json', 'w+') as file:
        file.write(json_recs)



