import pandas as pd
import numpy as np
import json
from tqdm import tqdm

from embeddings import book_embedding
from find_knn import find_knn

DIR = 'data'

def load_and_preprocess_pg_catalog(path=f'{DIR}/pg_catalog.csv'):
    df = pd.read_csv(path)
    df = df.fillna('nan')
    df.to_csv(f'{DIR}/pg_catalog_out.csv', index=False)
    return df

books_to_recommend_num = 50

df = load_and_preprocess_pg_catalog()

recommendations = {}
for i in range(len(df)):
    print(f'Book no. {i}')
    embeddings = []
    books = []
    for j in tqdm(range(i+1, len(df), 1)):
        embeddings.append(book_embedding(df.iloc[i], df.iloc[j]))
        books.append(df.iloc[j]['Title'])
        if j == 8:
            break
    indices = find_knn(books_to_recommend_num, embeddings, [[1 for _ in range(len(embeddings[0]))]])
    recommendations[df.iloc[i]['Title']] = np.take(np.array(books), indices).flatten().tolist()
    break

json_recs = json.dumps(recommendations)
with open('recommendations/book_recommendations.json', 'w') as file:
    file.write(json_recs)



