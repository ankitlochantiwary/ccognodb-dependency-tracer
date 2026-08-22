MATCH (s:Skill {name:$skill})<-[:HAS_SKILL]-(p:Person)
OPTIONAL MATCH (p)-[:HELD]->(r:Role)-[:REQUIRES]->(s)
WITH p, count(DISTINCT r) AS roleMatch
MATCH (p)-[:HAS_SKILL]->(ps:Skill)
RETURN p.id AS id, p.name AS name, p.title AS title,
       roleMatch, collect(DISTINCT ps.name) AS skills
ORDER BY roleMatch DESC, p.name LIMIT 12;
