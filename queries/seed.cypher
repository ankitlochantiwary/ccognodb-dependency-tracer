UNWIND $people AS person
MERGE (p:Person {id: person.id})
SET p.name = person.name, p.bio = person.bio
MERGE (r:Role {name: person.role})
MERGE (c:Company {name: person.company})
MERGE (p)-[:HAS_ROLE]->(r)
MERGE (p)-[:WORKS_AT]->(c)
WITH DISTINCT p, person
UNWIND person.skills AS skillName
MERGE (s:Skill {name: skillName})
MERGE (p)-[:HAS_SKILL {level: person.skill_levels[skillName]}]->(s)
WITH DISTINCT p, person
UNWIND person.projects AS proj
MERGE (pr:Project {id: proj.id})
SET pr.name=proj.name, pr.summary=proj.summary
MERGE (p)-[:BUILT]->(pr)
WITH DISTINCT person
UNWIND person.project_skills AS ps
MATCH (pr:Project {id: ps.project_id})
MATCH (s:Skill {name: ps.skill})
MERGE (pr)-[:USES_SKILL]->(s);

UNWIND $roles AS roleData
MERGE (r:Role {name: roleData.name})
SET r.description = roleData.description
WITH DISTINCT r, roleData
UNWIND roleData.skills AS skillName
MATCH (s:Skill {name: skillName})
MERGE (r)-[:REQUIRES]->(s);
