import json
from pathlib import Path

from .db import get_driver
from .queries import load_query

ROOT = Path(__file__).resolve().parent.parent
SEED_FILE = ROOT / 'data' / 'seed.json'
_seed_checked = False


def ensure_seeded():
    """Idempotently apply the tiny demo seed once per serverless cold start."""
    global _seed_checked
    if _seed_checked:
        return

    data = json.loads(SEED_FILE.read_text(encoding='utf-8'))
    statements = [s.strip() for s in load_query('seed.cypher').split(';') if s.strip()]

    with get_driver().session() as session:
        for statement in statements:
            session.run(statement, people=data['people'], roles=data['roles']).consume()

    _seed_checked = True


def _run(query, **params):
    ensure_seeded()
    with get_driver().session() as session:
        return session.run(query, **params).data()


def graph_summary():
    rows = _run(load_query('summary.cypher'))
    return rows[0] if rows else {'people': 0, 'skills': 0, 'projects': 0, 'roles': 0, 'companies': 0}


def list_people(search: str = ''):
    return _run(load_query('people.cypher'), search=search.strip())


def list_skills():
    return _run(load_query('skills.cypher'))


def person_profile(person_id: str):
    rows = _run(load_query('person_profile.cypher'), person_id=person_id)
    return rows[0] if rows else None


def recommendations(skill: str, target_role: str = ''):
    return _run(load_query('recommendations.cypher'), skill=skill.strip(), target_role=target_role.strip())


def shortest_learning_path(person_id: str, target_skill: str):
    return _run(load_query('learning_path.cypher'), person_id=person_id, target_skill=target_skill.strip())
