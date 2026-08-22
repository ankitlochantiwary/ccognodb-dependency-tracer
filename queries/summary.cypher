MATCH (p:Person) WITH count(p) AS people
MATCH (s:Skill) WITH people, count(s) AS skills
MATCH (pr:Project) WITH people, skills, count(pr) AS projects
MATCH (r:Role) WITH people, skills, projects, count(r) AS roles
MATCH (c:Company)
RETURN people, skills, projects, roles, count(c) AS companies;
