import logging
from typing import Any, Dict
from os import environ

import boto3

LOG_LEVEL = int(environ['LOG_LEVEL'])
TABLE_NAME = environ['TABLE_NAME']

logging.basicConfig()
logger = logging.getLogger('extract_wikipedia_link')
logger.setLevel(LOG_LEVEL)

dynamodb = boto3.client('dynamodb')


def handler(event: Dict[str, Any], _):
  try:
    wikidata_id = event['wikidata_id']
    wikipedia_link = event['wikipedia_link']
    author = event['author']
    book_id = event['book_id']
    wikidata_data = {k: {'S': str(v)} for k, v in event['wikidata_data'].items()}

    logger.info(f'Saving data for book ID {book_id}.')

    dynamodb.put_item(
        TableName=TABLE_NAME,
        Item={
            'book_id': {
                'N': str(book_id)
            },
            'author': {
                'S': author
            },
            'wikipedia_link': {
                'S': wikipedia_link
            },
            'wikidata_id': {
                'S': wikidata_id
            },
            **wikidata_data
        },
    )

    return {'statusCode': 200}
  except KeyError as ex:
    logger.error(ex)
    return {'statusCode': 400, 'error': str(ex)}
  except Exception as ex:
    logger.error(ex)
    return {'statusCode': 500, 'error': str(ex)}
