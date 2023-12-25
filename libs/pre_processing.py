from transformers import BertTokenizer
from nltk.corpus import stopwords
from ast import literal_eval
import re, os, sys, nltk
import tensorflow as tf
from os import environ
import pandas as pd

path = os.path.abspath(__file__)
path = path[:path.find('/libs')]
sys.path.insert(1, path)
from libs.extract_load_data import ExtractLoadSqLite as extl
nltk.download('stopwords')

class PreProcessing:
    """
    Class for performing preprocessing 
    -------

    Including:
    -------
    - Applying regular expressions
    - Category manipulation
    - Abbreviation substitution
    - ...

    
    Attributes:
    -------
    - abbreviations (dict): Dictionary of abbreviations to be replaced.
    - values_regex (dict): Dictionary of regular expressions to be applied.

    Public Methods:
    -------
    - change_abbreviations_sentence(txt): Replaces abbreviations in a single sentence.
    - change_abbreviations_dataframe(data, column): Replaces abbreviations in a DataFrame column.
    - apply_regex_sentence(txt): Applies regular expressions to a single sentence.
    - apply_regex_dataframe(dataframe, column): Applies regular expressions to a DataFrame column.
    - drop_size(dataframe, column, n_size): Removes rows where the number of tokens is less than n_size.
    - dropnan_and_lowercase(dataframe, column): Removes rows with NaN values and converts to lowercase.
    - set_category(dataframe, column): Converts values in a column to categories.

    """
    def __init__(self) -> None:
        path = 'neuralmind/bert-base-portuguese-cased'
        self.tokenizer = BertTokenizer.from_pretrained(path, do_lower_case=False)

        self.__extract = extl()

        self.abbreviations = {'ngm': 'Ninguém', 'sdds': 'saudades', 'sdd': 'saudade', 'tao': 'tão', 
                 'td': 'tudo', 'qd': 'quando', 'flw': 'falou', 'nte': 'noite', 'mds': 'meu deus',
                 'vms': 'vamos', 'q': 'que', 'd': 'de', 'bjs': 'beijos', 'so': 'só', 'gt': 'gente',
                 'vc': 'você', 'vcs':'vocês', 'pq': 'por que', 'tbm': 'também', 'gnt': 'gente',
                 'obg': 'obrigado',  'n': 'não', 'nao': 'não', 'blz': 'beleza', 'c': 'com', 'd': 'de',
                 'p': 'para', 'fds': 'fim de semana', 'aki': 'aqui', 'amg': 'amiga', 'ja': 'já',
                 'vlw': 'valeu', 'ate': 'até', 'cmg': 'comigo', 'pfv': 'por favor', 'oq': 'o que',
                 'msm': 'mesmo', 'tava': 'estava', 'ta': 'está', 'tá': 'está','to': 'estou', 'tô': 'estou','bj': 'beijo', 
                 'aff': 'irritação', 'ai': 'ai', 'mt': 'muito', 'mto': 'muito', 'hj': 'hoje', 'eh': 'é',
                 'ufa': 'alívio', 'dps': 'depois', 'qnd': 'quando', 'lt': 'luto', 'mlk': 'menino', 'la': 'lá', 
                 'serio': 'sério', 'tb': 'tudo bem', 'dms': 'demais', 'cm': 'com', 'vdd': 'verdade', 'dnv': 'de novo'}
        

        emoji_pattern = re.compile("["
                                    u"\U0001F600-\U0001F64F"
                                    u"\U0001F300-\U0001F5FF"
                                    u"\U0001F680-\U0001F6FF"
                                    u"\U0001F700-\U0001F77F"
                                    u"\U0001F780-\U0001F7FF"
                                    u"\U0001F800-\U0001F8FF"
                                    u"\U0001F900-\U0001F9FF"
                                    u"\U0001FA00-\U0001FA6F"
                                    u"\U0001FA70-\U0001FAFF"
                                    u"\U00002702-\U000027B0"
                                    u"\U000024C2-\U0001F251" 
                                    "]+", flags=re.UNICODE)
        self.values_regex = {emoji_pattern: "", r'#\S+': "", 
                            r'@\S+': "", r'[^\w\s,.:;?!-]': "",
                            r'\b[k]{2,}\b': "risada"}
    def decode_ids(self, token_ids):
        tokenizer = self.tokenizer
        return tokenizer.convert_ids_to_tokens(token_ids)

    def change_abbreviations_sentence(self, txt) -> str:
        """
        Replaces abbreviations in a single sentence.

        Parameters:
        - txt (str): The sentence to be processed.

        Returns:
        - str: The sentence after abbreviation substitution.
        """
        abbreviations = self.abbreviations
        try:
            txt = txt.replace("  ", ' ')
            for key, values in abbreviations.items():
                txt = re.sub(fr"\b{key}\b", values, txt.lower())
            return txt.replace("  ", ' ').strip()
        except Exception as error:
            print(error)
    

    def change_abbreviations_dataframe(self, data, column) -> pd.DataFrame:
        """
        Replaces abbreviations in a DataFrame column.

        Parameters:
        - data (pd.DataFrame): The DataFrame to be processed.
        - column (str): The name of the column to be processed.

        Returns:
        - pd.DataFrame: The DataFrame after abbreviation substitution.
        """
        try:
            for i in range(data.shape[0]):
                txt = data[column][i]
                data.at[i, column] = self.change_abbreviations_sentence(txt)
            return data
        except Exception as error:
            print(error)

    
    def apply_regex_sentence(self, txt) -> str:
        """
        Applies regular expressions to a single sentence.

        Parameters:
        - txt (str): The sentence to be processed.

        Returns:
        - str: The sentence after applying regular expressions.
        """
        try:
            values_regex = self.values_regex
            for key, values in values_regex.items():
                txt = re.sub(key, values, txt.lower())
            return txt
        except Exception as error:
            print(error)
    

    def apply_regex_dataframe(self, dataframe, column) -> pd.DataFrame:
        """
        Applies regular expressions to a DataFrame column.

        Parameters:
        - dataframe (pd.DataFrame): The DataFrame to be processed.
        - column (str): The name of the column to be processed.

        Returns:
        - pd.DataFrame: The DataFrame after applying regular expressions to the specified column.
        """
        try:
            for i in range(dataframe.shape[0]):
                txt = dataframe[column][i]
                dataframe.at[i, column] = self.apply_regex_sentence(txt)
            return dataframe
        except Exception as error:
            print(error)

    

    def drop_size(self, dataframe, column, n_size) -> pd.DataFrame:
        """
        Removes rows where the number of tokens is less than n_size in a DataFrame column.

        Parameters:
        - dataframe (pd.DataFrame): The DataFrame to be processed.
        - column (str): The name of the column to be processed.
        - n_size (int): The minimum number of tokens required.

        Returns:
        - pd.DataFrame: The DataFrame after removing rows based on token count.
        """
        try:
            index_rm = []
            for i in range(dataframe.shape[0]):
                txt = dataframe[column][i]
                if type(txt) == float: continue
                txt = re.sub(r'[^\w\s]', ' ', txt)
                list_token = txt.replace("  ", ' ').split(' ')
                if '' in list_token: list_token.remove('')
                if len(list_token) < n_size: index_rm.append(i)
            dataframe.drop(index_rm, inplace=True)
            dataframe.index = range(len(dataframe))
            return dataframe
        except Exception as error:
            print(error)
    

    def dropnan_and_lowercase(self, dataframe, column) -> pd.DataFrame:
        """
        Removes rows with NaN values and converts text in a DataFrame column to lowercase.

        Parameters:
        - dataframe (pd.DataFrame): The DataFrame to be processed.
        - column (str): The name of the column to be processed.

        Returns:
        - pd.DataFrame: The DataFrame after removing NaN rows and converting text to lowercase.
        """
        try:
            index_rm = []
            for i in range(dataframe.shape[0]):
                txt = dataframe[column][i]
                if type(txt) == float or str(txt.lower()) == 'nan': 
                    index_rm.append(i)
                    continue
                txt = txt.lower()
                dataframe.at[i, column] = txt
            dataframe.drop(index_rm, inplace=True)
            dataframe.index = range(len(dataframe))
            return dataframe
        except Exception as error:
            print(error)


    def set_category(self, dataframe, column) -> pd.DataFrame:
        """
        Converts values in a column to categories.

        Parameters:
        - dataframe (pd.DataFrame): The DataFrame to be processed.
        - column (str): The name of the column to be processed.

        Returns:
        - pd.DataFrame: The DataFrame after converting values to categories.
        """
        try:
            index_rm = []
            for i in range(dataframe.shape[0]):
                txt = dataframe[column][i]
                if type(txt) == float or str(txt.lower()) == 'nan': 
                    index_rm.append(i)
                    continue
                elif ',' in txt:
                    categories = txt.split(',')
                    dataframe.at[i, column] = int(categories[0])
                    values = dataframe.loc[i].to_dict()
                    values[column] = int(categories[-1])
                    df = pd.DataFrame([values])
                    dataframe = pd.concat([dataframe, df])
                else:
                    dataframe.at[i, column] = int(txt)
            dataframe.drop(index_rm, inplace=True)
            dataframe.index = range(len(dataframe))
            return dataframe
        except Exception as error:
            print(f'--> {dataframe[column][i]}', error)


    def _encode_sentence(self, txt) -> list: 
        tokenizer = self.tokenizer
        return tokenizer.convert_tokens_to_ids(tokenizer.tokenize(txt))


    def convert_to_tokenizer(self, dataframe, column) -> list:
        return [self._encode_sentence(sentence) for sentence in dataframe[column]]
        

    def shuffled_dataframe(self, dataframe) -> pd.DataFrame:
        return dataframe.sample(frac=1.0, random_state=42).reset_index(drop=True)

    def remove_stopwords_sentence(self, txt) -> str:
        """
        Remove stopwords from a given text string in Portuguese.

        Parameters:
        - txt (str): The input text from which stopwords will be removed.

        Returns:
        str: The input text with stopwords removed.

        Raises:
        Exception: Any exception that may occur during the process.
        """
        try:
            stopwords_pt = set(stopwords.words('portuguese'))
            removed_stopwords = [token for token in txt.split() if token.lower() not in stopwords_pt]
            return " ".join(removed_stopwords)
        except Exception as error:
            print(error)


    def remove_stopwords_dataframe(self, dataframe, column) -> pd.DataFrame:
        """
        Remove stopwords from a specific column in a DataFrame.

        Parameters:
        - dataframe (pd.DataFrame): The input DataFrame.
        - column (str): The name of the column from which stopwords will be removed.

        Returns:
        pd.DataFrame: The DataFrame with stopwords removed from the specified column.

        Raises:
        Exception: Any exception that may occur during the process.
        """
        try:
            for i in range(dataframe.shape[0]):
                txt = dataframe[column][i]
                txt = self.remove_stopwords_sentence(txt)
                dataframe.at[i, column] = txt
            return dataframe
        except Exception as error:
            print(error)