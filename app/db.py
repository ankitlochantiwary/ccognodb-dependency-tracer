from neo4j import GraphDatabase
from .config import COGNODB_URI, COGNODB_USER, COGNODB_PASSWORD, validate_config

_driver = None


def get_driver():
    global _driver
    validate_config()
    if _driver is None:
        _driver = GraphDatabase.driver(COGNODB_URI, auth=(COGNODB_USER, COGNODB_PASSWORD))
    return _driver


def run_query(query, **params):
    driver = get_driver()
    with driver.session() as session:
        return [record.data() for record in session.run(query, **params)]


def close_driver():
    global _driver
    if _driver:
        _driver.close()
        _driver = None
