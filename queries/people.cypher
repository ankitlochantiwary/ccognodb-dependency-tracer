MATCH (p:Person)-[:HAS_ROLE]->(r:Role), (p)-[:WORKS_AT]->(c:Company)
OPTIONAL MATCH (p)-[:HAS_SKILL]->(matchedSkill:Skill)
WITH p, r, c, matchedSkill
WHERE $search = ''
   OR toLower(p.name) CONTAINS toLower($search)
   OR toLower(r.name) CONTAINS toLower($search)
   OR toLower(c.name) CONTAINS toLower($search)
   OR (matchedSkill IS NOT NULL AND toLower(matchedSkill.name) CONTAINS toLower($search))
WITH DISTINCT p, r, c
OPTIONAL MATCH (p)-[:HAS_SKILL]->(allSkill:Skill)
RETURN p.id AS id,
       p.name AS name,
       r.name AS role,
       c.name AS company,
       count(DISTINCT allSkill) AS skill_count
ORDER BY p.name;
