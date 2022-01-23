import logging
from os import path, environ

import numpy as np
import pandas as pd

DIR = path.dirname(path.realpath(__file__))
LOG_LEVEL = int(environ['LOG_LEVEL'])

logging.basicConfig()
logger = logging.getLogger('drop_duplicates')
logger.setLevel(LOG_LEVEL)


def drop_duplicates(
    authors_file: str = path.join(DIR, '..', 'data', 'authors_wiki.csv'),
    unique_authors_file: str = path.join(DIR, '..', 'data', 'unique_authors_wiki.csv'),
):
  """
  Usuń zduplikowanych autorów.

  Args:
    authors_file(str): Ścieżka do pliku wejściowego.
    unique_authors_file(str): Ścieżka do pliku wyjściowego, z unikalnymi autorami.
  """
  df = pd.read_csv(authors_file)
  df.dropna(inplace=True, how='any', subset=['WikipediaLink'])
  df = df.drop_duplicates(subset=['Author'])

  df.to_csv(unique_authors_file, encoding='utf-8', index=False)
  df_split = np.array_split(df, 4)

  for idx, split in enumerate(df_split):
    pd.DataFrame(split).to_csv(unique_authors_file.replace('.csv', f'_{idx}.csv'), encoding='utf-8', index=False)


if __name__ == '__main__':
  drop_duplicates()
