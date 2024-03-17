-- Create the 'users' table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    spotify_user_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);


-- Create the 'liked_songs' table
CREATE TABLE liked_songs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    spotify_track_id VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Unique constraint to ensure a song is only liked once per user
ALTER TABLE liked_songs ADD UNIQUE INDEX idx_user_song (user_id, spotify_track_id);
