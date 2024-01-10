from os import environ
from time import sleep
import pandas as pd
import requests 
import os, sys

path = os.path.abspath(__file__)
path = path[:path.find('/scripts')]
sys.path.insert(1, path)
from libs.sqlite_manager import Sqlite as slq3



def _get_song(artist_name, song_name, api_url='https://api.vagalume.com.br/search.php') -> dict:
    """
    Retrieves the lyrics of a specific song by an artist using the Vagalume API.
    -------
    
    Args:
        - artist_name (str): The name of the artist.
        - song_name (str): The name of the song.
        - api_url (str): The URL of the Vagalume API. Default is 'https://api.vagalume.com.br/search.php'.
    
    Returns:
        - tuple: A tuple containing two dictionaries. The first dictionary contains information about the song, including the song name, the Vagalume song ID, the Vagalume song URL, and the lyrics of the song. The second dictionary contains information about the artist, including the artist's full name and the Vagalume artist ID.
        - If the song is not found, it returns (False, False).
    """
    try:
        params = {
            'art': artist_name,
            'mus': song_name,
            'apikey': environ['API_VAGALUME']
        }
        response = requests.get(api_url, params=params)
        sleep(2)

        print(response.url)
        results = response.json()
        if results['type'] == "song_notfound":
            print("NOT FOUND!!!")
        txt = results['mus'][0]
        music_name, music_id, music_href = txt['name'], txt['id'], txt['url']
        lyrics = txt['text']
        art_name, art_id = results['art']['name'], results['art']['id']
        list_lyrics = [i.strip() for i in lyrics.split('\n') if len(i) > 0]
        dict_song = {"song_name": music_name,
                     "vagalume_song_id": music_id,
                     "vagalume_song_url": music_href,
                     "lyrics": "|".join(list_lyrics)}
        
        dict_artist = {"artist_full_name": art_name,
                       "vagalume_artist_id": art_id}
        return dict_song, dict_artist
    except Exception as error:
        print(error)
        return False, False


def _insert_and_search(dataframe, slq3_instance) -> None:
    """
    Inserts the song and artist information into the SQLite database and performs a search for each song using the get_song function.
    ------
    Args:
        - dataframe (pandas.DataFrame): The DataFrame containing the list of songs and artists.
        - slq3_instance (libs.sqlite_manager.Sqlite): An instance of the Sqlite class from the libs package, responsible for connecting to and manipulating the SQLite database.
    """
    song_cols = str(("song_id", "song_name", "lyrics", "vagalume_song_url", "vagalume_song_id"))
    artist_cols = str(("artist_id", "song_id", "artist_full_name", "vagalume_artist_id"))
    artist_cols = artist_cols.replace("\'", '')
    try:
        for i in range(dataframe.shape[0]):

            song_name = dataframe.music_name[i]
            artist_name = dataframe.artist_name[i]
            print("SONG: ", i, song_name, artist_name)


        
            dict_song, dict_artist = _get_song(artist_name, song_name)
            if not dict_artist: continue


            values_song = [i]+list(dict_song.values())
            values_song = str(tuple(values_song))

            values_artist = [i]+list(dict_artist.values())
            values_artist.insert(1, i)
            values_artist = str(tuple(values_artist))

            song_query = f"INSERT INTO song {song_cols} VALUES {values_song};"
            slq3_instance.insert(query=song_query)
            artist_query = f"INSERT INTO artist {artist_cols} VALUES {values_artist};"
            slq3_instance.insert(query=artist_query)
            print()
            
            
    except Exception as error:
        print(i, error)
        print("-->", song_query)
        print("-->", artist_query)
        print("\n\n")


def main() -> None:
    """
    The main function that initializes the database connection, reads the list of songs from a CSV file,
    calls the insert_and_search function, and inserts the song and artist information into the database.
    """
    slq3_instance = slq3(database=environ['PATH_DATABASE'])
    dataframe = pd.read_csv(environ['PATH_SONGS_LIST'])
    _insert_and_search(dataframe, slq3_instance)

if __name__ == "__main__":
    main()
