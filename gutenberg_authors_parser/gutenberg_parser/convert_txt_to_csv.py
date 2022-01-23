import logging
from os import path, environ

import numpy as np
import pandas as pd

DIR = path.dirname(path.realpath(__file__))
LOG_LEVEL = int(environ['LOG_LEVEL'])

logging.basicConfig()
logger = logging.getLogger('convert_txt_to_csv')
logger.setLevel(LOG_LEVEL)


def convert_txt_to_csv(
    in_file: str = path.join(DIR, '..', 'data', 'authors_data.txt'),
    out_file: str = path.join(DIR, '..', 'data', 'authors_data.csv'),
):
  """
  Konwertuj plik z autorami z pliku txt (wynik działania `dynamodb_dump.sh`) do formatu csv.

  Args:
    in_file(str): Ścieżka do pliku w formacie txt (plik wejściowy)
    out_file(str): Ścieżka do pliku w formacie csv (plik wyjściowy)
  """
  df = pd.read_csv(in_file, sep='\t')
  df.replace('None', np.NaN, inplace=True)
  df.to_csv(out_file, encoding='utf-8', index=False)


if __name__ == '__main__':
  convert_txt_to_csv()
