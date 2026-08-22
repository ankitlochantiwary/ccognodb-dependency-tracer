SUMMARY = '''MATCH (n) WITH labels(n) AS labels UNWIND labels AS label RETURN label, count(*) AS count ORDER BY label'''

PEOPLE = '''MATCH (p:Person) WHERE $search = '' OR toLower(p.name) CONTAINS toLower($search) RETURN p.id AS id, p.name AS name, p.title AS title ORDER BY p.name'''

PROFILE = '''MATCH (p:Person {id:$person_id}) OPTIONAL MATCH (p)-[:HAS_SKILL]->(s:Skill) WITH p, collect(DISTINCT s.name) AS skills OPTIONAL MATCH (p)-[:WORKED_ON]->(pr:Project) WITH p, skills, collect(DISTINCT pr.name) AS projects OPTIONAL MATCH (p)-[:HELD]->(r:Role)-[:AT]->(c:Company) RETURN p.id AS id,p.name AS name,p.title AS title,skills,projects,collect(DISTINCT {role:r.title,company:c.name}) AS roles'''

RECOMMENDATIONS = '''MATCH (s:Skill {name:$skill})<-[:HAS_SKILL]-(p:Person) OPTIONAL MATCH (p)-[:HELD]->(r:Role)-[:REQUIRES]->(s) WITH p, count(DISTINCT r) AS roleMatch MATCH (p)-[:HAS_SKILL]->(ps:Skill) WITH p, roleMatch, collect(DISTINCT ps.name) AS skills RETURN p.id AS id,p.name AS name,p.title AS title,roleMatch,skills ORDER BY roleMatch DESC, p.name LIMIT 12'''

LEARNING_PATH = '''MATCH (p:Person {id:$person_id}), (target:Skill {name:$target_skill}) MATCH path=shortestPath((p)-[:HAS_SKILL|USED|WORKED_ON|REQUIRES*..8]-(target)) RETURN [n IN nodes(path) | coalesce(n.name,n.title,n.id)] AS path'''

SKILLS = '''MATCH (s:Skill) RETURN s.name AS name ORDER BY name'''

SCHEMA = '''CREATE CONSTRAINT person_id IF NOT EXISTS FOR (p:Person) REQUIRE p.id IS UNIQUE'''
'''
