from neo4j import GraphDatabase
from .config import settings

_driver = None


def get_driver():
    global _driver
    if _driver is None:
        if not settings.cognodb_uri or not settings.cognodb_password:
            raise RuntimeError('CognoDB is not configured. Set COGNODB_URI and COGNODB_PASSWORD.')
        _driver = GraphDatabase.driver(
            settings.cognodb_uri,
            auth=(settings.cognodb_user, settings.cognodb_password),
        )
    return _driver


def verify_connection():
    driver = get_driver()
    driver.verify_connectivity()


def close_driver():
    global _driver
    if _driver:
        _driver.close()
        _driver = None
