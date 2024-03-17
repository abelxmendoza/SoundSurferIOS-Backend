from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
# Configuration for Flask-MySQLdb
app.config['MYSQL_USER'] = 'your_mysql_username'
app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
app.config['MYSQL_DB'] = 'your_database_name'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# User functions
def create_user(spotify_user_id, email):
    cursor = mysql.connection.cursor()
    query = "INSERT INTO users (spotify_user_id, email) VALUES (%s, %s)"
    cursor.execute(query, (spotify_user_id, email))
    mysql.connection.commit()
    cursor.close()

def get_user_by_spotify_id(spotify_user_id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM users WHERE spotify_user_id = %s"
    cursor.execute(query, (spotify_user_id,))
    user = cursor.fetchone()
    cursor.close()
    return user

# Song functions
def like_song(spotify_user_id, spotify_track_id):
    cursor = mysql.connection.cursor()
    query = """
        INSERT INTO liked_songs (user_id, spotify_track_id)
        SELECT id, %s FROM users WHERE spotify_user_id = %s
    """
    cursor.execute(query, (spotify_track_id, spotify_user_id))
    mysql.connection.commit()
    cursor.close()

def unlike_song(spotify_user_id, spotify_track_id):
    cursor = mysql.connection.cursor()
    query = """
        DELETE liked_songs
        FROM liked_songs
        JOIN users ON liked_songs.user_id = users.id
        WHERE users.spotify_user_id = %s AND liked_songs.spotify_track_id = %s
    """
    cursor.execute(query, (spotify_user_id, spotify_track_id))
    mysql.connection.commit()
    cursor.close()

def get_liked_songs(spotify_user_id):
    cursor = mysql.connection.cursor()
    query = """
        SELECT liked_songs.spotify_track_id
        FROM liked_songs
        JOIN users ON liked_songs.user_id = users.id
        WHERE users.spotify_user_id = %s
    """
    cursor.execute(query, (spotify_user_id,))
    songs = cursor.fetchall()
    cursor.close()
    return songs
