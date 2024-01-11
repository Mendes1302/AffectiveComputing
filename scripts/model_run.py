from warnings import filterwarnings
import numpy as np
from joblib import load
import pandas as pd
import os, sys
filterwarnings("ignore")


path = os.path.abspath(__file__)
path = path[:path.find('/scripts')]
sys.path.insert(1, path)
from libs.pre_processing import PreProcessing 
from libs.sqlite_manager import Sqlite as slq3



def _insert_and_search(dataframe, slq3_instance) -> None:
    inputs_cols = str(("song_id", "song_name", "model_name", 
                       "emotion", "value")).replace("\'", "")
    try:
        for i in range(dataframe.shape[0]):
            song_id = dataframe['song_id'][i]
            song_name = dataframe['song_name'][i]
            model_name = dataframe['model_name'][i]
            emotion = dataframe['emotion'][i]
            value = dataframe['value'][i]

            values = str((song_id, song_name, model_name, 
                                  emotion, value))
            inputs_query = f"INSERT INTO emotional_result {inputs_cols} VALUES {values};"
            slq3_instance.insert(query=inputs_query)
            
            print(inputs_query)
            
    except Exception as error:
        print("-->", error)
        return None


def _preprocessing_train(dataframe, column) -> pd.DataFrame|list:
    pp = PreProcessing()
    for i in range(dataframe.shape[0]):
        txt = dataframe[column][i].replace('|', ' ')
        dataframe.at[i, column] = txt
    dataframe = pp.dropnan_and_lowercase(dataframe, column)
    dataframe = pp.change_abbreviations_dataframe(dataframe, column)
    dataframe = pp.drop_size(dataframe, column, 3)
    dataframe = pp.apply_regex_dataframe(dataframe, column)
    dataframe = pp.remove_stopwords_dataframe(dataframe, column)

    texts_val = dataframe.lyrics
    inputs_val = np.array([pp.convert_to_tokenizer(text, 512) for text in texts_val])

    return dataframe, inputs_val


def _fix_results(df) -> pd.DataFrame:
    array_cols = ['song_id', 'song_name', 'model_name','emotion', 'value']
    df_final = pd.DataFrame(columns=array_cols)
    for _, row in df.iterrows():
        song_name = row['song_name']
        song_id = int(row['song_id'])
        artist_full_name = row['artist_full_name']
        for emotion in df.columns[3:]:
            value = row[emotion]
            dict_values = {'song_id': song_id, 'song_name': song_name, 
                           'model_name': 'DCNN', 'artist_full_name':artist_full_name,
                           'emotion': emotion, 'value': value}
            df_final = df_final.append(dict_values, ignore_index=True)
    return df_final 


def main() -> None:
    model_path = path+'/model/DCNN.keras'
    model = load(model_path)

    database_path = path+'/songs_database.db'
    slq3_instance = slq3(database=database_path)
    
    query = 'SELECT song.song_id, song.song_name, song.lyrics, artist.artist_full_name FROM song INNER JOIN artist ON song.song_id = artist.song_id;'
    inputs = slq3_instance.get_by_select(query=query)
    songs, inputs_val =  _preprocessing_train(inputs, 'lyrics')

    emotion_name = slq3_instance.get_by_select(query="SELECT name_emotion FROM emotion;")
    emotion_name = emotion_name.to_dict()["name_emotion"]
    
    predicts = model.predict(inputs_val)
    df_results = pd.DataFrame(predicts, columns=[emotion_name[i] for i in range(len(emotion_name))])

    df_results = pd.concat([songs.drop(['lyrics'], axis=1), df_results], axis=1)
    df_final = _fix_results(df_results)

    df_final.to_csv("songs_results.csv", index=False)
    df_final.drop(["artist_full_name"], axis=1, inplace=True)

    _insert_and_search(df_final, slq3_instance)


if __name__ == "__main__": main()