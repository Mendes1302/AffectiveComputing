import pandas as pd
import sqlite3 

class Sqlite():
    """
    A class for interacting with SQLite database.
    -------
    Required modules:

    - pandas
    - sqlite3


    Attributes:
        - database (str): The path to the SQLite database file.
        - conn (sqlite3.Connection): The SQLite database connection.
        - cur (sqlite3.Cursor): The SQLite database cursor.
    
    Example:

    - get_by_select():

        >>> Sqlite(database_name.bd).get_by_select(query=query_select)

    - insert():

        >>> Sqlite(database_name.bd).insert(query=query_insert)

    - update():
    
        >>> Sqlite(database_name.bd).get_by_select(query=query_update)
    """ 
    def __init__(self, database) -> None:
        """
        Initialize the Sqlite instance.
        -------

        Args:
            - database (str): The path to the SQLite database file.
        """
        self.database = database
        self.conn, self.cur = self._connect()


    def _connect(self) -> sqlite3.Connection|sqlite3.Cursor:
        """
        Connect to the SQLite database.
        -------

        Returns:
            - tuple: A tuple containing the database connection and cursor.
        """
        try:
            self.conn = sqlite3.connect(self.database)
            self.cur = self.conn.cursor()
            return self.conn, self.cur
        except sqlite3.Error as error:
            print("Failed to connect:", error)


    def get_by_select(self, query) -> pd.DataFrame:
        """
        Execute a SELECT query and return the result as a DataFrame.
        -------

        Args:
            - query (str): The SELECT query to be executed.

        Returns:
            - data: A DataFrame containing the query result.
        """
        try:
            self.cur.execute(query)
            columns = [desc[0] for desc in self.cur.description]
            rows = self.cur.fetchall()
            data = pd.DataFrame(rows, columns=columns)
            return data
        except sqlite3.Error as error:
            print("Failed to insert:", error)
        self.cur.execute(query)


    def insert(self, query) -> None:
        """
        Execute an INSERT query to insert data into the database.
        -------

        Args:
            - query (str): The INSERT query to be executed.
        """
        try:
            self.cur.execute(query)
            self.conn.commit()
        except sqlite3.Error as error:
            print("Failed to insert:", error)


    def update(self, query) -> None:
        """
        Execute an UPDATE query to update data in the database.
        -------

        Args:
            - query (str): The UPDATE query to be executed.
        """
        try:
            self.cur.execute(query)
            self.conn.commit()
        except sqlite3.Error as error:
            print("Failed to insert:", error)