CREATE TABLE IF NOT EXISTS user_faces (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNSIGNED NOT NULL,
    name TEXT NOT NULL,
    encoding BLOB NOT NULL
) DEFAULT CHARSET=utf8 COLLATE=utf8_bin;