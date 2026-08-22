from .db import run_query
from .queries import SUMMARY, PEOPLE, PROFILE, RECOMMENDATIONS, LEARNING_PATH, SKILLS


def graph_summary():
    rows = run_query(SUMMARY)
    return {row['label']: row['count'] for row in rows}


def list_people(search=''):
    return run_query(PEOPLE, search=search)


def list_skills():
    return run_query(SKILLS)


def person_profile(person_id):
    rows = run_query(PROFILE, person_id=person_id)
    return rows[0] if rows else None


def recommendations(skill, target_role=''):
    return run_query(RECOMMENDATIONS, skill=skill, target_role=target_role)


def shortest_learning_path(person_id, target_skill):
    rows = run_query(LEARNING_PATH, person_id=person_id, target_skill=target_skill)
    return rows[0] if rows else {'path': []}
