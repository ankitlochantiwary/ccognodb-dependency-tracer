MATCH (p:Person)-[:HAS_ROLE]->(r:Role), (p)-[:WORKS_AT]->(c:Company)
OPTIONAL MATCH (p)-[:HAS_SKILL]->(s:Skill)
WITH p,r,c,count(DISTINCT s) AS skill_count
WHERE $search = '' OR toLower(p.name) CONTAINS toLower($search) OR toLower(r.name) CONTAINS toLower($search) OR EXISTS { MATCH (p)-[:HAS_SKILL]->(ss:Skill) WHERE toLower(ss.name) CONTAINS toLower($search) }
RETURN p.id AS id, p.name AS name, r.name AS role, c.name AS company, skill_count
ORDER BY p.name;
