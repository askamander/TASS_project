import json
import logging
from os import environ, path
from typing import Any, Dict, List, Optional

import boto3
import numpy as np
import pandas as pd

DIR = path.dirname(path.realpath(__file__))
LOG_LEVEL = int(environ['LOG_LEVEL'])
SCRAPER_LAMBDA = environ['SCRAPER_LAMBDA']

logging.basicConfig()
logger = logging.getLogger('extract_wikipedia_link')
logger.setLevel(LOG_LEVEL)

client = boto3.client('lambda')


def handler(event: Dict[str, Any], _):
  dataset_path = event['dataset_path']
  df = pd.read_csv(dataset_path)
  wikidata_ids: List[Optional[str]] = []
  for _, row in df.iterrows():
    logger.info(f'Processing author {row.get("Author", None)}. Book ID: {row.get("BookID", None)}')
    wikipedia_link = row.get('WikipediaLink', None)
    logger.debug(wikipedia_link)
    if wikipedia_link is np.NAN:
      logger.info('Wikipedia link is NaN, skipping...')
      wikidata_ids.append(None)
      continue

    try:
      client.invoke(
          FunctionName=SCRAPER_LAMBDA,
          InvocationType='Event',
          Payload=json.dumps({
              'wikipedia_link': wikipedia_link,
              'book_id': row.get("BookID", None),
              'author': row.get("Author", None),
          }),
      )
    except Exception as ex:
      logger.error(ex)
      return {'statusCode': 500, 'error': str(ex)}

  return {
      'statusCode': 200,
  }
