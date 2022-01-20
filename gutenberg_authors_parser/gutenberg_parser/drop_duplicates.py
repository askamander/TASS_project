import logging
from os import path, environ

import pandas as pd

DIR = path.dirname(path.realpath(__file__))
LOG_LEVEL = int(environ['LOG_LEVEL'])

logging.basicConfig()
logger = logging.getLogger('extract_wikipedia_link')
logger.setLevel(LOG_LEVEL)


def drop_duplicates(
    authors_file: str = path.join(DIR, '..', 'data', 'authors_wiki.csv'),
    unique_authors_file: str = path.join(DIR, '..', 'data', 'unique_authors_wiki.csv'),
    head_1000_unique_authors_file: str = path.join(DIR, '..', 'data', 'head_1000_unique_authors_wiki.csv'),
    head_1000_unique_authors_file_rest: str = path.join(DIR, '..', 'data', 'head_1000_unique_authors_wiki_rest.csv'),
):
  df = pd.read_csv(authors_file)
  df.dropna(inplace=True, how='any', subset=['WikipediaLink'])
  df = df.drop_duplicates(subset=['Author'])
  print(df.tail())

  df.to_csv(unique_authors_file, encoding='utf-8', index=False)
  first_1000_df = df[:1000]
  first_1000_rest_df = df[1000:]
  first_1000_df.to_csv(head_1000_unique_authors_file, encoding='utf-8', index=False)
  first_1000_rest_df = df[1000:]
  first_1000_rest_df.to_csv(head_1000_unique_authors_file_rest, encoding='utf-8', index=False)


if __name__ == '__main__':
  drop_duplicates()
