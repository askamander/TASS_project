import unittest
from TASS_project.embeddings import embeddings


# all combinations for years of live of 2 people
# b_a d_a b_b d_b
# b_a b_b d_a d_b
# b_a b_b d_b d_a
# b_b b_a d_b d_a
# b_b d_b b_a d_a
# b_b b_a d_a d_b

class TestStringMethods(unittest.TestCase):

    def test_jaccard_embedding(self):
        self.assertEqual(embeddings.jaccard_embedding(1, 3, 2, 4), 0)
        self.assertEqual(embeddings.jaccard_embedding(1, 2, 3, 4), 1 / 5)
        self.assertEqual(embeddings.jaccard_embedding(1, 2, 4, 3), 1 / 5)
        self.assertEqual(embeddings.jaccard_embedding(2, 1, 4, 3), 1 / 5)
        self.assertEqual(embeddings.jaccard_embedding(1, 3, 4, 2), 0)
        self.assertEqual(embeddings.jaccard_embedding(2, 1, 3, 4), 1 / 5)


if __name__ == '__main__':
    unittest.main()
