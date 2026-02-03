-- define a new user
INSERT INTO user (username, password) VALUES (
    "user1",
    "scrypt:32768:8:1$OevLVDM6PCp98g2c$d3b3743fe02093c60711c50e97f6805ae70c19293fa30465db7655c65b8200e23f69b22ff99477eed7226903ea1f415d18c10ce0ab0567d7c5d00353749f4aa0" -- password is "user"
);

-- define a new user
INSERT INTO user (username, password) VALUES (
    "user2",
    "scrypt:32768:8:1$OevLVDM6PCp98g2c$d3b3743fe02093c60711c50e97f6805ae70c19293fa30465db7655c65b8200e23f69b22ff99477eed7226903ea1f415d18c10ce0ab0567d7c5d00353749f4aa0" -- password is "user"
);

-- define a new post
-- INSERT INTO post (author_id, created, title, body) VALUES (

-- );