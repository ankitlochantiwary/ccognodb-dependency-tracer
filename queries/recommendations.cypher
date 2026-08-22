MATCH (selected:Skill {name: $skill})<-[:HAS_SKILL]-(p:Person)-[:HAS_ROLE]->(currentRole:Role),
      (p)-[:WORKS_AT]->(c:Company)
OPTIONAL MATCH (p)-[:BUILT]->(pr:Project)-[:USES_SKILL]->(selected)
WITH p, currentRole, c, count(DISTINCT pr) AS project_evidence,
     collect(DISTINCT pr.name) AS shared_projects
OPTIONAL MATCH (targetRole:Role)-[:REQUIRES]->(required:Skill)
WHERE $target_role <> '' AND toLower(targetRole.name) = toLower($target_role)
WITH p, currentRole, c, project_evidence, shared_projects, targetRole,
     collect(DISTINCT required) AS required_skills
OPTIONAL MATCH (p)-[:HAS_SKILL]->(matched:Skill)
WHERE matched IN required_skills
WITH p, currentRole, c, project_evidence, shared_projects, targetRole, required_skills,
     collect(DISTINCT matched.name) AS matched_role_skills
WHERE $target_role = '' OR targetRole IS NOT NULL
RETURN p.name AS name,
       currentRole.name AS role,
       c.name AS company,
       CASE
         WHEN $target_role = '' THEN CASE WHEN 50 + project_evidence * 25 > 100 THEN 100 ELSE 50 + project_evidence * 25 END
         WHEN size(required_skills) = 0 THEN 0
         ELSE toInteger(100.0 * size(matched_role_skills) / size(required_skills))
       END AS score,
       shared_projects,
       matched_role_skills,
       size(required_skills) AS required_skill_count
ORDER BY score DESC, name
LIMIT 12;
