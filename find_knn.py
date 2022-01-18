from sklearn.neighbors import NearestNeighbors
import numpy as np


def find_knn(num_of_neighbours, embeddings, target_embedding):
    nbrs = NearestNeighbors(n_neighbors=num_of_neighbours+1, algorithm='ball_tree').fit(embeddings)
    distances, indices = nbrs.kneighbors(target_embedding)
    return indices

if __name__ == '__main__':
    num_of_neighbours = 2
    embeddings = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
    target_embedding = np.array([[-1,-1]])
    print(find_knn(num_of_neighbours, embeddings, target_embedding))


