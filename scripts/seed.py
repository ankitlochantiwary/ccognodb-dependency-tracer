import json
import os
from pathlib import Path
from neo4j import GraphDatabase
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / '.env')
DATA = json.loads((ROOT / 'data' / 'seed.json').read_text(encoding='utf-8'))

uri = os.getenv('COGNODB_URI')
user = os.getenv('COGNODB_USER', 'cognodb')
password = os.getenv('COGNODB_PASSWORD')
if not uri or not password:
    raise SystemExit('Set COGNODB_URI and COGNODB_PASSWORD before seeding.')

def statements(path: Path):
    return [part.strip() for part in path.read_text(encoding='utf-8').split(';') if part.strip()]

driver = GraphDatabase.driver(uri, auth=(user, password))
try:
    with driver.session() as session:
        for statement in statements(ROOT / 'queries' / 'schema.cypher'):
            try:
                session.run(statement).consume()
            except Exception as exc:
                # Constraints improve integrity but are not required to load the demo data.
                # Keep the seed path usable if a CognoDB version omits a DDL feature.
                print(f'Schema warning: {exc}')
        for statement in statements(ROOT / 'queries' / 'seed.cypher'):
            session.run(statement, people=DATA['people'], roles=DATA['roles']).consume()
        count = session.run('MATCH (n) RETURN count(n) AS count').single()['count']
        print(count, 'nodes loaded')
finally:
    driver.close()
