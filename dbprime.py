import psycopg2

class MockRecord:
    '''
    Requires a python database module that conforms to the
    PEP-249 database API specification.

    Unpacks and inserts a database record based on the passed in kwargs.
    The initialized object contains the newly inserted primary key value.
    '''

    def __init__(self, database_module, database_args, table_name, primary_key_column, **kwargs):
        # Check if we can even handle the db module before trying anything else
        try:
            self.insertion_handler = \
                self.__class__.insertion_handlers[database_module.__name__]

        except KeyError:
            error_message = 'Unhandled database module: {} Supported modules: {}'\
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
        self.columns = sorted([kwargs.keys()])

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __del__(self):
        # delete inserted record
        # close db connection
        sql = 'DELETE FROM {} WHERE {} = {};'.format(self.table_name,
                                                     self.pk_column,
                                                     getattr(self, self.pk_column))
        self._db_cursor.execute(sql)
        self._db_connection.close()

    def _insert_postgres_record(self):
        # insert a record into the db using the db connection
        # set the value of the primary key as an attr on the object instance
        sql = """
            INSERT INTO {} ({})
            VALUES ({})
            RETURNING {};
        """.format(self.table_name,
                   ', '.join(self.columns),
                   ', '.join([getattr(self, key) for key in self.columns]))

        self._db_cursor.execute(sql)

        primary_key = self._db_cursor.fetchone()[0]
        setattr(self, self.pk_column, primary_key)

    def _insert_mysql_record(self):
        # insert a record into the db using the db connection
        # set the value of the primary key as an attr on the object instance
        pass

    insertion_handlers = {
        'psycopg2': _insert_postgres_record,
        'MySQLdb': _insert_mysql_record,
    }

def test():
    dbargs = {
        'user': 'test',
        'password': 'test',
        'db': '',
        'host': ''
    }
    mock_rec = MockRecord(psycopg2, dbargs, 'test_table', 'test_tableid')

if __name__ == '__main__':
    test()
