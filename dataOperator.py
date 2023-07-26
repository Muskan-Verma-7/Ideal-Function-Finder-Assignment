import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
import os
from dbConnection import DBConnector


class InvalidFileError(Exception):
    """
    Exception raised when an invalid file path is passed.

    Attributes:
        file_path (str): The file path that caused the error.
        error_message (str): An error message.
    """

    def __init__(self, file_path, error_message="is not valid"):
        """
        Initialize the InvalidFileError instance.

        Args:
            file_path (str): The file path that caused the error.
            error_message (str, optional): An error message. Defaults to "is not valid".
        """
        self.file_path = file_path
        self.error_message = f"File path {file_path} {error_message}"
        super().__init__(self.error_message)


def handle_errors(func):
    """
    A helper function to handle errors for various operations.

    Args:
        func (function): The function to wrap.

    Returns:
        function: The wrapped function.
    """

    def wrapper(*args, **kwargs):
        """
        The wrapper function.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Any: The result of the function call.
        """
        try:
            return func(*args, **kwargs)
        except (SQLAlchemyError, pd.errors.ParserError) as e:
            print(f"Failed to execute {func.__name__}: {str(e)}")
            return None

    return wrapper


class DataOperator(DBConnector):
    """
    Class to handle data operations on a MySQL database.
    """

    @handle_errors
    def fetch_data(self, db_table):
        """
        Fetches the data from the specified table in the database and returns a pandas dataframe.

        Args:
            db_table (str): The name of the database table to fetch.

        Returns:
            DataFrame: The table data as a pandas DataFrame.
        """
        with self.establish_engine().connect() as connection:
            return pd.read_sql_table(db_table, connection)

    def load_csv(self, csv_path):
        """
        Loads a CSV file and returns a pandas dataframe.

        Args:
            csv_path (str): The path to the CSV file to load.

        Returns:
            DataFrame: The CSV data as a pandas DataFrame.
        """
        if not os.path.isfile(csv_path):
            raise InvalidFileError(csv_path)
        return self._read_csv(csv_path)

    @handle_errors
    def _read_csv(self, csv_path):
        """
        Reads a CSV file and returns a pandas dataframe.

        Args:
            csv_path (str): The path to the CSV file to read.

        Returns:
            DataFrame: The CSV data as a pandas DataFrame.
        """
        return pd.read_csv(csv_path, index_col=0)

    @handle_errors
    def save_to_database(self, data_frame, db_table):
        """
        Saves a pandas dataframe in a MySQL database.

        Args:
            data_frame (DataFrame): The pandas DataFrame to save.
            db_table (str): The name of the database table to save the data in.
        """
        with self.establish_engine().connect() as connection, connection.begin():
            data_frame.to_sql(db_table, connection, if_exists="replace")

    def handle_datasets(self, dataset_paths):
        """
        Loads all training datasets and saves them in the MySQL database.

        Args:
            dataset_paths (list[str]): A list of file paths to the training datasets.
        """
        for dataset_path in dataset_paths:
            data_frame = self.load_csv(dataset_path)
            if data_frame is not None:
                db_table = os.path.splitext(os.path.basename(dataset_path))[0]
                self.save_to_database(data_frame, db_table)
