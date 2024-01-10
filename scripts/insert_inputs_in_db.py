from os import environ
import pandas as pd
import os, sys

path = os.path.abspath(__file__)
path = path[:path.find('/scripts')]
sys.path.insert(1, path)
from libs.sqlite_manager import Sqlite as slq3
from libs.pre_processing import PreProcessing

pp = PreProcessing()

def _preprocessing(dataframe, column, source, emotion_id='emotion_id')-> pd.DataFrame:
    """
    Preprocesses the input DataFrame by applying various transformations.
    
    Parameters:
    - dataframe: Pandas DataFrame - The input data to be preprocessed.
    - column: str - The name of the column containing the text data.
    - source: str - The source identifier for the data (e.g., 'tweets' or 'ChatGPT').
    - emotion_id: str (default='emotion_id') - The name of the column containing emotion labels.
    
    Returns:
    - dataframe - The preprocessed DataFrame with columns renamed and various transformations applied.
    """
    try: 
        if source == 'tweets':
            dataframe = pp.set_category(dataframe, emotion_id)
        dataframe = pp.dropnan_and_lowercase(dataframe, column)
        dataframe = pp.change_abbreviations_dataframe(dataframe, column)
        dataframe = pp.drop_size(dataframe, column, 3)
        dataframe = pp.apply_regex_dataframe(dataframe, column)
        dataframe = pp.shuffled_dataframe(dataframe)
        dataframe = pp.remove_stopwords_dataframe(dataframe, column)

        dataframe['source'] = [source for _ in range(dataframe.shape[0])]
        dataframe.rename({column: 'text_name', emotion_id: 'emotion_id'}, axis=1, inplace=True)
        return dataframe
    except Exception as error:
        print(error)
        return None


def _insert_and_search(dataframe, slq3_instance=0) -> None:
    """
    Inserts the preprocessed data into the 'inputs' table of the SQLite database.
    
    Parameters:
    - dataframe: Pandas DataFrame - The preprocessed data to be inserted into the database.
    - slq3_instance: SQLite instance - An instance of the SQLite manager for database operations.
    
    Returns:
    - None - Inserts the data into the database and does not return anything.
    """
    inputs_cols = str(("text_name", "source", "emotion_id"))
    try:
        for i in range(dataframe.shape[0]):

            text_name = dataframe.text_name[i]
            source = dataframe.source[i]
            emotion_id = dataframe.emotion_id[i]

            values_inputs = str((text_name, source, emotion_id))

            inputs_query = f"INSERT INTO inputs {inputs_cols} VALUES {values_inputs};"
            slq3_instance.insert(query=inputs_query)
            
            
    except Exception as error:
        print(i, error)
        print("-->", inputs_query)
        print("\n\n")


def _tweets() -> pd.DataFrame:
    """
    Reads and preprocesses tweet data from a CSV file.
    
    Returns:
    - tweets - The preprocessed DataFrame containing tweet data.
    """
    path = environ['PATH_TEST_DATASET']
    tweets = pd.read_csv(path, delimiter='\t')
    tweets.drop(['tweet_id'], axis=1, inplace=True)
    tweets = _preprocessing(tweets, column="tweet", source="tweets", emotion_id="categoria")
    return tweets


def _chatGPT(slq3_instance) -> pd.DataFrame:
    """
    Reads and preprocesses text data related to different emotions from ChatGPT.
    
    Parameters:
    - slq3_instance: SQLite instance - An instance of the SQLite manager for database operations.
    
    Returns:
    - dataframe - The preprocessed DataFrame containing ChatGPT-generated text data.
    """

    query = "SELECT name_emotion FROM emotion"
    emotions = slq3_instance.get_by_select(query)
    emotions = emotions.to_dict()["name_emotion"]
    emotions = {v: k for k, v in emotions.items()}

    labels = list(emotions.keys())
    labels.remove('confusão') 

    for emotion in labels:
        file = f'/home/lucas/AffectiveComputing/data_source/phrases_about_emotion/{emotion}.txt'
        values = []
        with open(file, 'r') as love:
            txts = love.read()
            for txt in txts.split('\n'):
                values.append(txt)

        dict_emotion = {
            'text_name': values,
            'emotion_id': [emotions[emotion]  for _ in range(len(values))]
        }
        if emotion == labels[0]:
            dataframe = pd.DataFrame(dict_emotion)
            dataframe.drop_duplicates(subset=['text_name'], inplace=True)
        df = pd.DataFrame(dict_emotion)
        df.drop_duplicates(subset=['text_name'], inplace=True)
        
        dataframe = pd.concat([df, dataframe])
        dataframe.index = range(dataframe.shape[0])
    dataframe.dropna(subset=['text_name'], inplace=True)
    dataframe = _preprocessing(dataframe, column='text_name', source='ChatGPT')
    return dataframe


    
def main() -> None:
    """
    The main function that initializes the SQLite manager, processes tweet and ChatGPT data,
    and inserts the preprocessed data into the SQLite database.
    
    Returns:
    - None - Executes the main functionality of the script and does not return anything.
    """
    path = environ['PATH_DATABASE']
    slq3_instance = slq3(database=path)

    tweets = _tweets()
    chatgpt = _chatGPT(slq3_instance)

    _insert_and_search(tweets, slq3_instance)
    _insert_and_search(chatgpt, slq3_instance)
       
    
if __name__ == "__main__":
    main()