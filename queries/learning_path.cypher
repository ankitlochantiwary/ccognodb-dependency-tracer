MATCH (p:Person {id:$person_id}), (target:Skill {name:$target_skill})
MATCH path=shortestPath((p)-[:HAS_SKILL|USED|WORKED_ON|REQUIRES*..8]-(target))
RETURN [n IN nodes(path) | coalesce(n.name,n.title,n.id)] AS path;
