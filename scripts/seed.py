import json
from pathlib import Path
from app.db import run_query

CREATE='''MATCH (n) DETACH DELETE n
CREATE (a:Person {id:'p1',name:'Anika Shah',title:'Senior Backend Engineer'}),(b:Person {id:'p2',name:'Rohan Mehta',title:'Data Engineer'}),(c:Person {id:'p3',name:'Maya Rao',title:'Platform Engineer'}),
(s1:Skill {name:'Python'}),(s2:Skill {name:'Neo4j'}),(s3:Skill {name:'GraphQL'}),(s4:Skill {name:'AWS'}),(s5:Skill {name:'Docker'}),(s6:Skill {name:'TypeScript'}),
(pr1:Project {name:'Talent Graph'}),(pr2:Project {name:'Data Platform'}),(pr3:Project {name:'API Gateway'}),
(r1:Role {title:'Backend Engineer'}),(r2:Role {title:'Data Engineer'}),(r3:Role {title:'Platform Engineer'}),
(co1:Company {name:'Northstar Labs'}),(co2:Company {name:'Orbit Systems'}),
(a)-[:HAS_SKILL]->(s1),(a)-[:HAS_SKILL]->(s2),(a)-[:HAS_SKILL]->(s5),(b)-[:HAS_SKILL]->(s1),(b)-[:HAS_SKILL]->(s4),(b)-[:HAS_SKILL]->(s3),(c)-[:HAS_SKILL]->(s2),(c)-[:HAS_SKILL]->(s5),(c)-[:HAS_SKILL]->(s6),
(a)-[:WORKED_ON]->(pr1),(b)-[:WORKED_ON]->(pr2),(c)-[:WORKED_ON]->(pr3),(pr1)-[:USED]->(s2),(pr2)-[:USED]->(s4),(pr3)-[:USED]->(s3),
(a)-[:HELD]->(r1),(b)-[:HELD]->(r2),(c)-[:HELD]->(r3),(r1)-[:AT]->(co1),(r2)-[:AT]->(co2),(r3)-[:AT]->(co1),
(r1)-[:REQUIRES]->(s1),(r1)-[:REQUIRES]->(s2),(r2)-[:REQUIRES]->(s4),(r2)-[:REQUIRES]->(s3),(r3)-[:REQUIRES]->(s2),(r3)-[:REQUIRES]->(s5)'''
run_query(CREATE)
print('Seed complete')
