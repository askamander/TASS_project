import logging
from os import path
import os
from typing import Optional, Tuple

from rdflib import Graph

DIR = path.dirname(path.realpath(__file__))
LOG_LEVEL = int(os.environ['LOG_LEVEL'])

logging.basicConfig()
logger = logging.getLogger('extract_wikipedia_link')
logger.setLevel(LOG_LEVEL)


def extract_wikipedia_link(file_path: str) -> Tuple[Optional[str], Optional[str]]:
  """
  Extract wikipedia link from RDF file.

  Args:
    file_path (str): Path to RDF file.

  Returns:
    (Tuple[Optional[str], Optional[str]]): Tuple of author's name and wikipedia link.
  """
  g = Graph()
  try:
    g.parse(file_path, format="xml")
  except FileNotFoundError as err:
    logger.error(err)
    return None, None

  book_query = """
    SELECT ?book_id
    WHERE {
     ?book_id a pgterms:ebook ;
    }"""

  book_query_result = g.query(book_query)
  assert len(book_query_result) >= 1
  if len(book_query_result) > 1:
    logger.warning(f'Number of rows in the book_query_result exceeds 1. Got {len(book_query_result)} rows.')
  book_id = [row.book_id for row in book_query_result][0]
  logger.debug(f'Book ID URI: {book_id}')

  creator_query = """
    SELECT ?creator_id
    WHERE {
     ?book_id dcterms:creator ?creator_id ;
    }"""

  creator_query_result = g.query(creator_query, initBindings={'book_id': book_id})
  if len(creator_query_result) > 1:
    logger.warning(f'Number of rows in the creator_query_result exceeds 1. Got {len(creator_query_result)} rows.')
  if len(creator_query_result) == 0:
    logger.warning(f'No creator was found for the book with ID: {book_id}.')
    return None, None
  creator_id = [row.creator_id for row in creator_query_result][0]
  logger.debug(f'Creator ID URI: {creator_id}')

  name_query = """
    SELECT ?name
    WHERE {
      ?agent_id pgterms:name ?name ;
    }"""
  name_query_result = g.query(name_query, initBindings={'agent_id': creator_id})
  assert len(name_query_result) == 1
  name = [row.name for row in name_query_result][0]

  wikipedia_link_query = """
    SELECT ?link
    WHERE {
      ?agent_id pgterms:webpage ?link ;
    }"""

  wikipedia_link_query_result = g.query(wikipedia_link_query, initBindings={'agent_id': creator_id})
  wikipedia_links = [row.link for row in wikipedia_link_query_result if 'wikipedia' in row.link]
  if len(wikipedia_links) == 0:
    logger.warning(f'No wikipedia link was found for the author with ID: {creator_id}.')
    return name, None
  elif len(wikipedia_links) > 1:
    logger.debug(f'Wikipedia links: {wikipedia_links}')
    logger.warning('Number of wikipedia links in the creator_query_result exceeds 1. '
                   f'Got {len(creator_query_result)} rows. Returning first link')

  logger.debug(f'Wikipedia link: {wikipedia_links[0]}')

  return str(name), str(wikipedia_links[0])


def construct_path(book_id: int) -> str:
  return path.join(DIR, '..', 'cache', 'epub', str(book_id), f'pg{book_id}.rdf')


if __name__ == '__main__':
  book_id = 808
  file_path = construct_path(book_id)
  logger.info(f'Wikipedia link: {extract_wikipedia_link(file_path)}')
