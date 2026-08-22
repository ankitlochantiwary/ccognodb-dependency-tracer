MATCH (n) WITH labels(n) AS labels UNWIND labels AS label RETURN label, count(*) AS count ORDER BY label;
