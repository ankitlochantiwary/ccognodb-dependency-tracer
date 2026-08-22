# CognoDB SkillGraph

A graph-native talent explorer built for the CognoDB assignment. It models people, skills, projects, roles, and companies as a connected graph and uses parameterized Cypher for multi-hop exploration, recommendations, and learning paths.

## Architecture

Browser UI -> FastAPI -> Neo4j Python Driver -> CognoDB

Nodes: Person, Skill, Project, Role, Company.
Relationships: HAS_SKILL, WORKED_ON, HELD, AT, REQUIRES, USED.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# set COGNODB_URI, COGNODB_USER, COGNODB_PASSWORD
python scripts/seed.py
uvicorn app.main:app --reload
```

Open http://localhost:8000.

## Features

- Graph overview
- Search people
- Person profile with skills/projects/roles
- Skill-based talent recommendations
- Multi-hop learning path from a person to a target skill
- Parameterized Cypher throughout
- Database error and empty-result states
- Docker deployment configuration

## Security

Never commit `.env` or database credentials. Configure CognoDB secrets in the hosting provider's environment settings.
