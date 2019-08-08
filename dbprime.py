

class MockRecord:
    '''
    Requires a database connection object that conforms to the
    PEP-249 database API specification.

    Unpacks and inserts a database record based on the passed in kwargs.
    The initialized object contains the newly inserted primary key value.
    '''

    def __init__(self, db_connection, primary_key_column, **kwargs):
        self.db_connection = db_connection
        self.primary_key_column = primary_key_column

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __del__(self):
        pass
