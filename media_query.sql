SELECT
    p.post_id,
    u.username,
    p.title,
    p.published_at
FROM posts AS p
JOIN users AS u ON u.user_id = p.user_id
WHERE p.published_at >= '2026-02-05 00:00:00'
  AND p.published_at < '2026-02-11 00:00:00'
ORDER BY p.published_at;
