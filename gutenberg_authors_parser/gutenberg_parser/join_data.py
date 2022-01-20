import logging
from os import path, environ

import pandas as pd

DIR = path.dirname(path.realpath(__file__))
LOG_LEVEL = int(environ['LOG_LEVEL'])

logging.basicConfig()
logger = logging.getLogger('join_data')
logger.setLevel(LOG_LEVEL)


def join_data(
    authors_wiki_file: str = path.join(DIR, '..', 'data', 'authors_wiki.csv'),
    authors_data_file: str = path.join(DIR, '..', 'data', 'authors_data.csv'),
    books_file: str = path.join(DIR, '..', 'data', 'parsed_pg_catalog.csv'),
    out_file: str = path.join(DIR, '..', 'data', 'pg_authors.csv'),
):
  authors_wiki_df = pd.read_csv(authors_wiki_file)
  authors_wiki_df.rename(columns={'Author': 'CreatorName', 'BookID': 'Text#'}, inplace=True)

  authors_data_df = pd.read_csv(authors_data_file)
  authors_data_df.drop(['Author', 'WikipediaLink'], axis=1, inplace=True)
  authors_data_df.rename(columns={'BookId': 'Text#'}, inplace=True)

  books_df = pd.read_csv(books_file)

  df = pd.merge(books_df, authors_wiki_df, on='Text#', how='outer')
  df = pd.merge(df, authors_data_df, on='Text#', how='outer')
  print(df.head(50))
  df.to_csv(out_file, encoding='utf-8', index=False)


if __name__ == '__main__':
  join_data()
