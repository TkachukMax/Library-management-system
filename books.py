from db_table import DbTable


class Books(DbTable):
    """
    Represents the 'books' table in the database with methods to perform CRUD operations.

    Attributes:
        name (str): The name of the table.
        _attributes (str): The attributes of the table.
        insert_order (list): The order of attributes for insert operations.
    """
    name = "books"
    _attributes = """
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100) NOT NULL,
    year INT NOT NULL,
    status VARCHAR(10) NOT NULL
    """
    insert_order = ["title", "author", "year", "status"]

    def create_object(self, *args):
        """
        Generates a SQL query to insert a new book into the 'books' table.

        Args:
            *args: The values to insert into the table (title, author, year).

        Returns:
            tuple: SQL query to insert a new book and the provided values.
        """
        return f"""
        INSERT INTO {self.name} ({', '.join(self.insert_order)})
        VALUES ({('%s,'*(len(self.insert_order)-1))[:-1:]}, 'в наличии');
        """, args
