import json
import logging
from os import environ, path
from time import sleep
from typing import Any, Dict, List, Optional

import boto3
import numpy as np
import pandas as pd

DIR = path.dirname(path.realpath(__file__))
LOG_LEVEL = int(environ['LOG_LEVEL'])
SCRAPER_LAMBDA = environ['SCRAPER_LAMBDA']
DATASET_PATH = environ['DATASET_PATH']

logging.basicConfig()
logger = logging.getLogger('extract_wikipedia_link')
logger.setLevel(LOG_LEVEL)

client = boto3.client('lambda')


def handler(event: Dict[str, Any], _):
    df = pd.read_csv(DATASET_PATH)
    wikidata_ids: List[Optional[str]] = []
    for _, row in df.iterrows():
        logger.info(
            f'Processing author {row.get("Author", None)}. Book ID: {row.get("BookID", None)}'
        )
        wikipedia_link = row.get('WikipediaLink', None)
        logger.debug(wikipedia_link)
        if wikipedia_link is np.NAN:
            logger.info('Wikipedia link is NaN, skipping...')
            wikidata_ids.append(None)
            continue

        try:
            response: Dict[str, Any] = client.invoke(
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

        # payload = response['Payload']
        # resolved_payload = json.loads(json.loads(payload.read().decode("utf-8"))['body'])
        # logger.debug(f'Got response from lambda: {str(resolved_payload)}')
        # wikidata_id = resolved_payload.get('wikidata_id', None)
        # logger.info(f'Wikidata ID: {wikidata_id}')
        # wikidata_ids.append(wikidata_id)

    # df['wikidata_id'] = pd.Series(wikidata_ids, index=df.index, copy=False)
    # df.to_csv('new_test.csv', encoding='utf-8', index=False)

    return {
        'statusCode': 200,
    }
