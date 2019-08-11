import psycopg2

class MockRecord:
    '''
    Requires a python database module that conforms to the
    PEP-249 database API specification.

    Each MockRecord object creates and closes its own db connection so the user
    doesn't have to be concerned with connection management while writing tests.

    Unpacks and inserts a database record based on the passed in kwargs.
    The initialized object contains the newly inserted primary key value.
    '''

    def __init__(self, database_module, database_args, table_name, primary_key_column, **kwargs):
        # Check if we can even handle the db module before trying anything else
        try:
            self.insertion_handler = \
                self.__class__.insertion_handlers[database_module.__name__]

        except KeyError:
            error_message = 'Unhandled database module: {} \n Supported modules: {}'\
                .format(database_module.__name__,
                        self.__class__.insertion_handlers.keys())

            raise KeyError(error_message)

        try:
            self._db_connection = database_module.connect(**database_args)
            self._db_cursor = self._db_connection.cursor()
        except Exception as e:
            print(e)
            raise

        self.table_name = table_name
        self.pk_column = primary_key_column
        self.columns = sorted(list(kwargs.keys()))
        if not self.columns:
            raise Exception('Can\'t insert a database record with no values. ' \
                'You have to specify columns/values in the kwargs of MockRecord...')

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.insertion_handler(self)

    def __del__(self):
        # We're going to assume that if the object doesn't have a primary key set
        # that we failed to insert the record in the first place.
        if hasattr(self, self.pk_column):
            try:
                sql = 'DELETE FROM {} WHERE {} = {};'.format(self.table_name,
                                                             self.pk_column,
                                                             getattr(self, self.pk_column))
                self._db_cursor.execute(sql)
            except Exception as e:
                print(e)

        self._db_connection.close()

    def _insert_postgres_record(self):
        sql = """
            INSERT INTO {} ({})
            VALUES ({})
            RETURNING {};
        """.format(self.table_name,
                   ', '.join(self.columns),
                   ', '.join([str(getattr(self, key)) for key in self.columns]),
                   self.pk_column)

        self._insert_record(sql)

    def _insert_mysql_record(self):
        pass

    def _insert_record(self, sql):
        '''
        Takes a database-specific sql string as an arg.
        Inserts a new database record, returning and setting the primary key
        as an attribute on the object.
        '''
        self._db_cursor.execute(sql)
        primary_key = self._db_cursor.fetchone()[0]
        setattr(self, self.pk_column, primary_key)

    insertion_handlers = {
        'psycopg2': _insert_postgres_record,
        'MySQLdb': _insert_mysql_record,
    }

def test():
    dbargs = {
        'user': 'ddirk',
        'password': 'test',
        'database': 'test_db',
        'host': 'localhost'
    }

    mock_rec = MockRecord(psycopg2, dbargs, 'test_table', 'test_tableid')

if __name__ == '__main__':
    test()
