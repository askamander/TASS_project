import json
import logging
from typing import Any, Dict
import requests
from os import path, environ

from bs4 import BeautifulSoup

DIR = path.dirname(path.realpath(__file__))
LOG_LEVEL = int(environ['LOG_LEVEL'])

logging.basicConfig()
logger = logging.getLogger('extract_wikipedia_link')
logger.setLevel(LOG_LEVEL)


def handler(event: Dict[str, Any], _):
  try:
    url = event['wikipedia_link']
    logger.info(f'Scraping wikidata ID for URL {url}.')
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    wikidata_item = soup.find(id='t-wikibase').find('a', href=True)
    wikidata_id = str(wikidata_item['href']).split('/')[-1]
    logger.info(f'Found ID: {wikidata_id}.')
    return {'statusCode': 200, 'body': json.dumps({'wikidata_id': wikidata_id})}
  except KeyError as ex:
    logger.error(ex)
    return {'statusCode': 400, 'error': str(ex)}
  except Exception as ex:
    logger.error(ex)
    return {'statusCode': 500, 'error': str(ex)}
