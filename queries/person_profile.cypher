MATCH (p:Person {id: $person_id})-[:HAS_ROLE]->(r:Role), (p)-[:WORKS_AT]->(c:Company)
OPTIONAL MATCH (p)-[:HAS_SKILL]->(s:Skill)
WITH p,r,c,collect(DISTINCT s.name) AS skills
OPTIONAL MATCH (p)-[:BUILT]->(pr:Project)
WITH p,r,c,skills,collect(DISTINCT {name: pr.name, summary: pr.summary}) AS projects
RETURN p.id AS id, p.name AS name, p.bio AS bio, r.name AS role, c.name AS company, skills, projects;
