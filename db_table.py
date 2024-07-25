from abc import ABC


class DbTable(ABC):
    """
    Abstract base class for database table operations.

    Attributes:
        name (str): The name of the table.
        attributes (str): The attributes of the table.
        insert_order (list): The order of attributes for insert operations.
    """
    name: str = ...
    attributes: str = ...
    insert_order: list = ...

    def create_if_not_exists(self) -> str:
        """
        Generates a SQL query to create the table if it does not already exist.

        Returns:
            str: SQL query to create the table.
        """
        return f"""
        
        CREATE TABLE IF NOT EXISTS {self.name} (
        {self.attributes}
        );
        """

    def create_object(self, *args):
        """
        Generates a SQL query to insert a new object into the table.

        Args:
            *args: The values to insert into the table.

        Returns:
            tuple: SQL query to insert a new object and the provided values.
        """
        return f"""
        INSERT INTO {self.name} ({', '.join(self.insert_order)})
        VALUES ({('%s,' * len(self.insert_order))[:-1:]});
        """, args

    def delete_object(self, object_id):
        """
        Generates a SQL query to delete an object from the table by its ID.

        Args:
            object_id (str): The ID of the object to delete.

        Returns:
            tuple: SQL query to delete the object and the provided ID.
        """
        return f"""
        DELETE 
        FROM {self.name}
        WHERE id = {object_id};
        """

    def search_object(self, attribute, value):
        """
        Generates a SQL query to search for an object in the table by a specific attribute.

        Args:
            attribute (str): The attribute to search by.
            value (str): The value of the attribute to search for.

        Returns:
            str: SQL query to search for the object.
        """
        return f"""
        SELECT * FROM {self.name}
        WHERE {attribute} = '{value}';
        """

    def show_all_object(self):
        """
        Generates a SQL query to retrieve all objects from the table.

        Returns:
            str: SQL query to retrieve all objects.
        """
        return f"""
        SELECT * FROM {self.name};
        """

    def change_status(self, object_id, value):
        """
        Generates a SQL query to update the status of an object in the table.

        Args:
            object_id (str): The ID of the object to update.
            value (str): The new status value.

        Returns:
            str: SQL query to update the object's status.
        """
        return f"""
        UPDATE {self.name} SET status = '{value}'
        WHERE id = {object_id}
        """

    def presence_object_by_id(self, id_object):
        """
        Generates a SQL query to check if an object exists in the table by its ID.

        Args:
            id_object (str): The ID of the object to check for existence.

        Returns:
            str: SQL query to check if the object exists.
        """
        return f"""
        SELECT
        EXISTS(SELECT * FROM {self.name} WHERE id = {id_object} )
        """
