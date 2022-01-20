import logging
from os import path, environ

import pandas as pd

from gutenberg_parser.extract_wikipedia_links import (
    extract_wikipedia_link,
    construct_path as construct_metadata_path,
)

DIR = path.dirname(path.realpath(__file__))
LOG_LEVEL = int(environ['LOG_LEVEL'])

logging.basicConfig()
logger = logging.getLogger('extract_wikipedia_link')
logger.setLevel(LOG_LEVEL)


def parse_book_data(
    file_path: str,
    parsed_pg_catalog_file: str = path.join(DIR, '..', 'data', 'parsed_pg_catalog.csv'),
    authors_file: str = path.join(DIR, '..', 'data', 'authors_wiki.csv'),
):
  df = pd.read_csv(file_path)
  # Remove NaN-s from authors
  df.dropna(inplace=True, how='any', subset=['Authors'])
  # Remove non-text entities, remove books with `Various` authors.
  df = df[(df['Type'] == 'Text') & (df['Authors'] != 'Various') & (df['Authors'] != 'Unknown')]

  authors_arr = []
  for _, book in df.iterrows():
    logger.info(f"Processing book {book['Title']} (ID: {book['Text#']})")
    book_metadata_path = construct_metadata_path(book['Text#'])
    author_name, author_wikipedia_link = extract_wikipedia_link(book_metadata_path)
    logger.debug(f"Author's Wikipedia link: {author_wikipedia_link}")
    authors_arr.append({'Author': author_name, 'BookID': book['Text#'], 'WikipediaLink': author_wikipedia_link})

  authors_df = pd.DataFrame(authors_arr)

  df.to_csv(parsed_pg_catalog_file, encoding='utf-8', index=False)
  authors_df.to_csv(authors_file, encoding='utf-8', index=False)


def construct_path() -> str:
  return path.join(DIR, '..', 'data', 'pg_catalog.csv')


if __name__ == '__main__':
  pd_catalog_path = construct_path()
  parse_book_data(pd_catalog_path)
