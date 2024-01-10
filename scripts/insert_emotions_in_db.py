from os import environ
import pandas as pd
import os, sys

path = os.path.abspath(__file__)
path = path[:path.find('/scripts')]
sys.path.insert(1, path)
from libs.sqlite_manager import Sqlite as slq3



def _get_emotions(file) -> dict:
    """
    Arranges the path and synonym file.
    -------
    
    Args:
        - file (str): Path the list of emotion from a TXT file.
    
    Returns:
        - dict: A dict containing information about the id_emotion, emotion and synonym.
        - If error, it returns False
    """
    try:
        list_emotion = []
        list_synonym = []
        with open(file, 'r') as synonym:
            txts = synonym.read()
            for txt in txts.split('\n'):
                values = txt.split(':')
                list_emotion.append(values[0].lower())
                list_synonym.append(values[1].replace(' ', '').split(';')[1:])
        dict_synonym = {
            'emotion': list_emotion,
            'synonym': list_synonym
        }
        
        return dict_synonym
    except Exception as error:
        print(error)
        return False


def _insert_and_search(dataframe, slq3_instance) -> None:
    """
    Inserts the emotion information into the SQLite database.
    ------
    Args:
        - dataframe (pandas.DataFrame): The DataFrame containing the list of emotion.
        - slq3_instance (libs.sqlite_manager.Sqlite): An instance of the Sqlite class from the libs package, responsible for connecting to and manipulating the SQLite database.
    """
    emotion_cols = str(("emotion_id", "name_emotion", "synonym_emotion"))
    try:
        for i in range(dataframe.shape[0]):

            emotion = dataframe.emotion[i]
            synonym = dataframe.synonym[i]
            print("EMOTION: ", i, emotion)

            values_emotion = str((i, emotion, str(synonym)))

            emotion_query = f"INSERT INTO emotion {emotion_cols} VALUES {values_emotion};"
            slq3_instance.insert(query=emotion_query)
            
            
    except Exception as error:
        print(i, error)
        print("-->", emotion_query)
        print("\n\n")


def main() -> None:
    """
    The main function that initializes the database connection, reads the list of emotion from a TXT file,
    calls the emotions_dict function, and inserts the emotion information into the database.
    """

    slq3_instance = slq3(database=environ['PATH_DATABASE'])
    emotions_dict = _get_emotions(environ['PATH_EMOTIONS'])
    dataframe = pd.DataFrame(emotions_dict)


    _insert_and_search(dataframe, slq3_instance)
    
    
if __name__ == "__main__":
    main()