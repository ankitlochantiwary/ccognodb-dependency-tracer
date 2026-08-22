MATCH (p:Person {id:$person_id})
OPTIONAL MATCH (p)-[:HAS_SKILL]->(s:Skill)
WITH p, collect(DISTINCT s.name) AS skills
OPTIONAL MATCH (p)-[:WORKED_ON]->(pr:Project)
WITH p, skills, collect(DISTINCT pr.name) AS projects
OPTIONAL MATCH (p)-[:HELD]->(r:Role)-[:AT]->(c:Company)
RETURN p.id AS id,p.name AS name,p.title AS title,skills,projects,
       collect(DISTINCT {role:r.title,company:c.name}) AS roles;
