import json
import os
from pathlib import Path
from neo4j import GraphDatabase

ROOT = Path(__file__).resolve().parent.parent
PEOPLE = json.loads((ROOT / 'data' / 'seed.json').read_text())

uri = os.getenv('COGNODB_URI')
user = os.getenv('COGNODB_USER', 'cognodb')
password = os.getenv('COGNODB_PASSWORD')
if not uri or not password:
    raise SystemExit('Set COGNODB_URI and COGNODB_PASSWORD before seeding.')

driver = GraphDatabase.driver(uri, auth=(user, password))
with driver.session() as session:
    for statement in (ROOT / 'queries' / 'schema.cypher').read_text().split(';'):
        statement = statement.strip()
        if statement:
            session.run(statement)
    session.run((ROOT / 'queries' / 'seed.cypher').read_text(), people=PEOPLE['people'], roles=PEOPLE['roles'])
    print(session.run('MATCH (n) RETURN count(n) AS count').single()['count'], 'nodes loaded')
driver.close()
