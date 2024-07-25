import psycopg2
from typing import Tuple


class DataBase:
    """
    A class to manage database connections and execute SQL queries.

    Attributes:
        connection: The database connection object.
        config (dict): The configuration for the database connection.
    """

    connection = None

    def __init__(self, *args, **kwargs):
        """
        Initializes the DataBase class with configuration parameters.

        Args:
            *args: Additional positional arguments.
            **kwargs: Configuration parameters for the database connection.
                dbname (str): Name of the database. Defaults to 'library'.
                host (str): Database host address. Defaults to '127.0.0.1'.
                user (str): Database user. Defaults to 'postgres'.
                password (str): User's password. Defaults to 'postgres'.
                port (str): Connection port number. Defaults to '5432'.
        """
        self.config = {
            'dbname': kwargs.get('dbname', 'library'),
            'host': kwargs.get('host', '127.0.0.1'),
            'user': kwargs.get('user', 'postgres'),
            'password': kwargs.get('password', 'postgres'),
            'port': kwargs.get('port', '5432')
        }
        self.__get_connection()

    def __get_connection(self):
        """
        Establishes a connection to the PostgreSQL server.

        Returns:
            None
        """
        psycopg2.connect(**self.config)

        try:
            # connecting to the PostgreSQL server
            with psycopg2.connect(**self.config) as conn:
                print('Connected to the PostgreSQL server.')
                self.connection = conn
        except (psycopg2.DatabaseError, Exception) as error:
            print(f"Error: {error}")

    @staticmethod
    def __dictfetchall(cursor) -> list:
        """
        Converts all rows from a cursor fetch operation into a dictionary.

        Args:
            cursor: The database cursor.

        Returns:
            List[dict]: A list of dictionaries representing the rows fetched.
        """
        """Преобразует все строки из результата запроса в Словарь"""
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]

    def execute_sql_query(self, query: str | Tuple[str, Tuple], fetch_description: bool = True):
        """
        Executes a SQL query on the database.

        Args:
            query (Union[str, Tuple[str, Tuple]]): The SQL query to execute.
            fetch_description (bool): Whether to fetch the description of the results. Defaults to True.

        Returns:
            Union[List[dict], None]: The fetched results if fetch_description is True, otherwise None.
        """
        with self.connection.cursor() as cur:
            try:
                if isinstance(query, str):
                    cur.execute(query)
                else:
                    cur.execute(*query)
                self.connection.commit()

                if fetch_description:
                    return self.__dictfetchall(cur)

            except Exception as e:
                print(f"Error: {e}\n{query}")
                self.connection.rollback()
