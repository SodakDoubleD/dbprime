

class MockRecord:
    '''
    Requires a database connection object that conforms to the
    PEP-249 database API specification.

    Unpacks and inserts a database record based on the passed in kwargs.
    The initialized object contains the newly inserted primary key value.
    '''

    insertion_handlers = {
        'psycopg2': insert_postgres_record,
        'MySQLdb': insert_mysql_record,
    }

    def __init__(self, database_module, database_args, primary_key_column, **kwargs):
        self._db_connection = database_module.connect(**database_args)
        self._db_cursor = self._db_connection.cursor()
        self._pk_column = primary_key_column
        try:
            self.insertion_handler = self.__class__.insertion_handlers[database_module.__name__]
        except KeyError:
            print('Unhandled database module: {}'.format(database_module.__name__))
            print('Supported modules: {}'.format(self.__class__.insertion_handlers.keys()))

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __del__(self):
        # delete inserted record
        # close db connection
        pass

    def insert_postgres_record(self):
        # insert a record into the db using the db connection
        # set the value of the primary key as an attr on the object instance
        pass

    def insert_mysql_record(self):
        # insert a record into the db using the db connection
        # set the value of the primary key as an attr on the object instance
        pass
