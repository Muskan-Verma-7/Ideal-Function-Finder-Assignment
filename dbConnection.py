from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError


class InvalidInputError(Exception):
    """
    This class is a custom exception that is used to indicate that there was an error with an input in a function call.

    Attributes:
        input_name (str): The name of the input that caused the error.
        error_message (str): An optional error message.
    """

    def __init__(self, input_name, error_message="is not valid"):
        """
        The constructor for the InvalidInputError class.

        Parameters:
            input_name (str): The name of the input that caused the error.
            error_message (str): An optional error message.
        """
        self.input_name = input_name
        self.error_message = f"Input {input_name} {error_message}"
        super().__init__(self.error_message)


class DBConnector:
    """
    This class handles the details of connecting to a database.

    Attributes:
        __database_url (str): The URL of the database.
        __database_name (str): The name of the database.
        __username (str): The username to use when connecting to the database.
        __password (str): The password to use when connecting to the database.
    """

    def __init__(self, database_url, database_name, username, password):
        """
        The constructor for the DBConnector class.

        Parameters:
            database_url (str): The URL of the database.
            database_name (str): The name of the database.
            username (str): The username to use when connecting to the database.
            password (str): The password to use when connecting to the database.

        Raises:
            InvalidInputError: If any of the inputs are None or empty.
        """

        # Validate the input parameters
        if not database_url or not database_name or not username or not password:
            raise InvalidInputError(
                "database_url/database_name/username/password",
                "cannot be None or empty",
            )

        self.__database_url = database_url
        self.__database_name = database_name
        self.__username = username
        self.__password = password

    def establish_engine(self):
        """
        This method creates and returns a database engine.

        Returns:
            Engine: A SQLAlchemy Engine instance.

        Raises:
            SQLAlchemyError: If there was a problem creating the engine.
        """
        try:
            return create_engine(
                f"mysql+pymysql://{self.__username}:{self.__password}@{self.__database_url}/{self.__database_name}"
            )
        except SQLAlchemyError as e:
            print(f"Failed to establish the database engine: {str(e)}")
            return None
