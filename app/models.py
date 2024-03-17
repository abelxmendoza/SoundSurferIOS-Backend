from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
# Configuration for Flask-MySQLdb
app.config['MYSQL_USER'] = 'your_mysql_username'
app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
app.config['MYSQL_DB'] = 'your_database_name'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # This is optional, it allows the cursor to return the query result as a dictionary

mysql = MySQL(app)

# User
def create_user(username, email):
    cursor = mysql.connection.cursor()
    query = "INSERT INTO users (username, email) VALUES (%s, %s)"
    cursor.execute(query, (username, email))
    mysql.connection.commit()
    cursor.close()

def get_user_by_id(user_id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()
    cursor.close()
    return user

# Song
def create_song(title, artist, album, playlist_id):
    cursor = mysql.connection.cursor()
    query = "INSERT INTO songs (title, artist, album, playlist_id) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (title, artist, album, playlist_id))
    mysql.connection.commit()
    cursor.close()

def get_song_by_id(song_id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM songs WHERE id = %s"
    cursor.execute(query, (song_id,))
    song = cursor.fetchone()
    cursor.close()
    return song

# Playlist
def create_playlist(name, user_id):
    cursor = mysql.connection.cursor()
    query = "INSERT INTO playlists (name, user_id, created_at) VALUES (%s, %s, NOW())"
    cursor.execute(query, (name, user_id))
    mysql.connection.commit()
    cursor.close()

def get_playlist_by_id(playlist_id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM playlists WHERE id = %s"
    cursor.execute(query, (playlist_id,))
    playlist = cursor.fetchone()
    cursor.close()
    return playlist
