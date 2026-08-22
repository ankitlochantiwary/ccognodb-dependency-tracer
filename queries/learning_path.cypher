MATCH (p:Person {id: $person_id}), (target:Skill {name: $target_skill})
MATCH path = shortestPath((p)-[:HAS_SKILL|BUILT|USES_SKILL*..8]-(target))
WITH path
RETURN [n IN nodes(path) | coalesce(n.name, n.id)] AS nodes, length(path) AS hops;
