import json
import logging
import sys
from enum import Enum
from os import environ
from typing import Any, Dict, List, Optional, Tuple, Union

import boto3
from SPARQLWrapper import SPARQLWrapper, JSON

LOG_LEVEL = int(environ['LOG_LEVEL'])
WIKIDATA_API_URL = environ['WIKIDATA_API_URL']
SAVE_DATA_LAMBDA = environ['SAVE_DATA_LAMBDA']

logging.basicConfig()
logger = logging.getLogger('extract_wikipedia_link')
logger.setLevel(LOG_LEVEL)

client = boto3.client('lambda')


class Properties(str, Enum):
  DateOfBirth = 'P569'
  DateOfDeath = 'P570'
  CountryOfCitizenship = 'P27'
  Occupation = 'P106'
  LanguagesSpokenWrittenOrSigned = 'P1412'
  Genre = 'P136'
  FieldOfWork = 'P101'
  MemberOf = 'P463'
  EducatedAt = 'P69'
  InfluencedBy = 'P737'


def query_wikidata(endpoint_url, query):
  user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
  sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
  sparql.setQuery(query)
  sparql.setReturnFormat(JSON)
  return sparql.query().convert()


def get_property(id: str,
                 property: Properties,
                 limit: Optional[int] = 1) -> Optional[Union[str, List[Tuple[str, str]]]]:
  logger.info(f'Querying {property.name} for ID {id}.')
  query = f"""
    SELECT ?statementValue ?statementValueLabel ?rank
    WHERE {{
        wd:{id} p:{property.value} ?statement .
        ?statement ps:{property.value} ?statementValue .
        ?statement wikibase:rank ?rank .
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    ORDER BY DESC(?rank)
    {f'LIMIT {limit}' if limit else ''}
    """
  results = query_wikidata(WIKIDATA_API_URL, query)
  parsed_results = [
      (
          r['statementValue']['value'].split('/')[-1],  # Get Wikidata ID
          r['statementValueLabel']['value'],
      ) for r in results["results"]["bindings"]
  ]
  if len(parsed_results) == 1:
    return parsed_results[0][1]
  elif len(parsed_results) > 1:
    return parsed_results
  logger.warning(f'No results found for property {property.name} for ID {id}.')
  return None


def handler(event: Dict[str, Any], _):
  try:
    wikidata_id = event['wikidata_id']
    wikipedia_link = event['wikipedia_link']
    author = event['author']
    book_id = event['book_id']
    logger.info(f'Quering wikidata for ID {wikidata_id}.')

    date_of_birth = get_property(id=wikidata_id, property=Properties.DateOfBirth)
    logger.debug(f'{date_of_birth=}')
    date_of_death = get_property(id=wikidata_id, property=Properties.DateOfDeath)
    logger.debug(f'{date_of_death=}')
    country_of_citizenship = get_property(id=wikidata_id, property=Properties.CountryOfCitizenship)
    logger.debug(f'{country_of_citizenship=}')
    occupation = get_property(id=wikidata_id, property=Properties.Occupation)
    logger.debug(f'{occupation=}')
    languages_spoken_written_or_signed = get_property(id=wikidata_id,
                                                      property=Properties.LanguagesSpokenWrittenOrSigned)
    logger.debug(f'{languages_spoken_written_or_signed=}')
    genre = get_property(id=wikidata_id, property=Properties.Genre)
    logger.debug(f'{genre=}')
    field_of_work = get_property(id=wikidata_id, property=Properties.FieldOfWork)
    logger.debug(f'{field_of_work=}')
    member_of = get_property(id=wikidata_id, property=Properties.MemberOf)
    logger.debug(f'{member_of=}')
    educated_at = get_property(id=wikidata_id, property=Properties.EducatedAt)
    logger.debug(f'{educated_at=}')
    influenced_by = get_property(id=wikidata_id, property=Properties.InfluencedBy, limit=None)
    logger.debug(f'{influenced_by=}')

    result = {
        'date_of_birth': date_of_birth,
        'date_of_death': date_of_death,
        'country_of_citizenship': country_of_citizenship,
        'occupation': occupation,
        'languages_spoken_written_or_signed': languages_spoken_written_or_signed,
        'genre': genre,
        'field_of_work': field_of_work,
        'member_of': member_of,
        'educated_at': educated_at,
        'influenced_by': influenced_by,
    }

    client.invoke(
        FunctionName=SAVE_DATA_LAMBDA,
        InvocationType='Event',
        Payload=json.dumps({
            'wikidata_data': result,
            'wikidata_id': wikidata_id,
            'wikipedia_link': wikipedia_link,
            'book_id': book_id,
            'author': author,
        }),
    )

    return {'statusCode': 200, 'body': json.dumps({'wikidata_data': result})}
  except KeyError as ex:
    logger.error(ex)
    return {'statusCode': 400, 'error': str(ex)}
  except Exception as ex:
    logger.error(ex)
    return {'statusCode': 500, 'error': str(ex)}
