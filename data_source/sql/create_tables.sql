

CREATE TABLE song(song_id INTEGER PRIMARY KEY NOT NULL, 
                  song_name TEXT NOT NULL, 
                  lyrics TEXT NOT NULL, 
                  vagalume_song_url TEXT NOT NULL, 
                  vagalume_song_id TEXT NOT NULL);




CREATE TABLE artist(artist_id INTEGER PRIMARY KEY NOT NULL, 
                  song_id INTEGER NOT NULL, 
                  artist_full_name TEXT NOT NULL, 
                  vagalume_artist_id TEXT NOT NULL,
                  FOREIGN KEY(song_id) REFERENCES song(song_id));


SELECT * FROM song
INNER JOIN artist ON song.song_id = artist.song_id;

SELECT * FROM artist;