from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text
import pandas as pd
from dbConnection import DBConnector


class InvalidTableError(Exception):
    """
    Exception raised when an invalid table name is passed.

    Attributes:
        table (str): The table name that caused the error.
        error_message (str): An error message.
    """

    def __init__(self, table, error_message="is not valid"):
        """
        Initialize the InvalidTableError instance.

        Args:
            table (str): The table name that caused the error.
            error_message (str, optional): An error message. Defaults to "is not valid".
        """
        self.table = table
        self.error_message = f"Table name {table} {error_message}"
        super().__init__(self.error_message)


class DataInspector(DBConnector):
    """
    Class to inspect data from a MySQL database.
    """

    def inspect_data(self, db_table):
        """
        Loads the data from the specified table name in the database
        and inspects it using Pandas functions.

        Args:
            db_table (str): The name of the database table to read and inspect.

        Raises:
            InvalidTableError: If the table name is None or empty.
        """
        if not db_table:
            raise InvalidTableError(db_table, "cannot be None or empty")

        try:
            with self.establish_engine().connect() as connection:
                query = text(f"SELECT * FROM {self._DBConnector__db_name}.{db_table}")
                data_frame = pd.read_sql(query, connection)
                self._print_data_info(data_frame, db_table)
        except SQLAlchemyError as e:
            print(f"Failed to inspect the data: {str(e)}")

    @staticmethod
    def _print_data_info(data_frame, db_table):
        """
        Prints information about the data.

        Args:
            data_frame (DataFrame): The pandas DataFrame to inspect.
            db_table (str): The name of the database table.
        """
        print(f"Data ({db_table}) info:\n")
        print(data_frame.info())
        print(f"\nData ({db_table}) shape:\n")
        print(data_frame.shape)
        print(f"Data ({db_table}) head:\n")
        print(data_frame.head())
        print(f"Data ({db_table}) description:\n")
        print(data_frame.describe())
