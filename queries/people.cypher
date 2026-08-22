MATCH (p:Person)
WHERE $search = '' OR toLower(p.name) CONTAINS toLower($search)
RETURN p.id AS id, p.name AS name, p.title AS title
ORDER BY p.name;
