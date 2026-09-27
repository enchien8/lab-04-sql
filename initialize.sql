-- Case Study 1 schema and seed data.
-- INSERT IGNORE makes these fixed-key seed rows safe to rerun without
-- replacing existing data or dropping unrelated rows.

CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
    post_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    body TEXT NOT NULL,
    published_at DATETIME NOT NULL,
    CONSTRAINT fk_posts_user
        FOREIGN KEY (user_id) REFERENCES users (user_id)
);

INSERT IGNORE INTO users (user_id, username, email, created_at)
VALUES (1, 'ada_lovelace', 'ada.lovelace@example.com', '2026-01-05 09:00:00');
INSERT IGNORE INTO users (user_id, username, email, created_at)
VALUES (2, 'alan_turing', 'alan.turing@example.com', '2026-01-06 09:15:00');
INSERT IGNORE INTO users (user_id, username, email, created_at)
VALUES (3, 'grace_hopper', 'grace.hopper@example.com', '2026-01-07 10:30:00');
INSERT IGNORE INTO users (user_id, username, email, created_at)
VALUES (4, 'donald_knuth', 'donald.knuth@example.com', '2026-01-08 11:45:00');
INSERT IGNORE INTO users (user_id, username, email, created_at)
VALUES (5, 'katherine_johnson', 'katherine.johnson@example.com', '2026-01-09 12:00:00');
INSERT IGNORE INTO users (user_id, username, email, created_at)
VALUES (6, 'margaret_hamilton', 'margaret.hamilton@example.com', '2026-01-10 13:20:00');
INSERT IGNORE INTO users (user_id, username, email, created_at)
VALUES (7, 'tim_berners_lee', 'tim.berners.lee@example.com', '2026-01-11 14:10:00');
INSERT IGNORE INTO users (user_id, username, email, created_at)
VALUES (8, 'radia_perlman', 'radia.perlman@example.com', '2026-01-12 15:05:00');
INSERT IGNORE INTO users (user_id, username, email, created_at)
VALUES (9, 'linus_torvalds', 'linus.torvalds@example.com', '2026-01-13 16:25:00');
INSERT IGNORE INTO users (user_id, username, email, created_at)
VALUES (10, 'maya_johnson', 'maya.johnson@example.com', '2026-01-14 17:40:00');

INSERT IGNORE INTO posts (post_id, user_id, title, body, published_at)
VALUES (101, 1, 'Notes on algorithms', 'A short introduction to algorithmic thinking.', '2026-02-01 09:00:00');
INSERT IGNORE INTO posts (post_id, user_id, title, body, published_at)
VALUES (102, 2, 'Computing machines', 'Questions about computation can guide useful designs.', '2026-02-02 09:30:00');
INSERT IGNORE INTO posts (post_id, user_id, title, body, published_at)
VALUES (103, 3, 'Reliable software', 'Testing and clear documentation improve reliability.', '2026-02-03 10:00:00');
INSERT IGNORE INTO posts (post_id, user_id, title, body, published_at)
VALUES (104, 4, 'Structured data', 'Schemas help teams reason about shared data.', '2026-02-04 10:30:00');
INSERT IGNORE INTO posts (post_id, user_id, title, body, published_at)
VALUES (105, 5, 'Measurements matter', 'Careful measurements support sound conclusions.', '2026-02-05 11:00:00');
INSERT IGNORE INTO posts (post_id, user_id, title, body, published_at)
VALUES (106, 6, 'Engineering practice', 'Small, repeatable steps make complex work manageable.', '2026-02-06 11:30:00');
INSERT IGNORE INTO posts (post_id, user_id, title, body, published_at)
VALUES (107, 7, 'Open standards', 'Shared standards make information easier to exchange.', '2026-02-07 12:00:00');
INSERT IGNORE INTO posts (post_id, user_id, title, body, published_at)
VALUES (108, 8, 'Network design', 'Thoughtful network design improves resilience.', '2026-02-08 12:30:00');
INSERT IGNORE INTO posts (post_id, user_id, title, body, published_at)
VALUES (109, 9, 'Collaborative tools', 'Collaborative tools help communities build software.', '2026-02-09 13:00:00');
INSERT IGNORE INTO posts (post_id, user_id, title, body, published_at)
VALUES (110, 10, 'Learning in public', 'Sharing lessons can help the next learner.', '2026-02-10 13:30:00');
