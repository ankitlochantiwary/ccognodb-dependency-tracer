MATCH (s:Skill {name: $skill})<-[:HAS_SKILL]-(p:Person)-[:HAS_ROLE]->(r:Role), (p)-[:WORKS_AT]->(c:Company)
OPTIONAL MATCH (p)-[:BUILT]->(pr:Project)-[:USES_SKILL]->(s)
WITH p,r,c,count(DISTINCT pr) AS project_evidence, collect(DISTINCT pr.name) AS shared_projects
WHERE $target_role = '' OR r.name = $target_role OR EXISTS { MATCH (r)-[:REQUIRES]->(target:Skill) WHERE target.name = $skill }
RETURN p.name AS name, r.name AS role, c.name AS company, (50 + project_evidence * 25) AS score, shared_projects
ORDER BY score DESC, name
LIMIT 12;
