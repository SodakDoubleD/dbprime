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
        try:
            self._db_connection = database_module.connect(**database_args)
        except Exception as e:
            print(e)
            raise

        self._db_cursor = self._db_connection.cursor()
        self.table_name = table_name
        self.pk_column = primary_key_column
        self.columns = sorted(list(kwargs.keys()))
        if not self.columns:
            raise Exception('Can\'t insert a database record with no values. ' \
                'You have to specify columns/values in the kwargs of MockRecord...')

        for key, value in kwargs.items():
            setattr(self, key, value)

        self._insert_record()
        self._set_primary_key_attribute()

    def __del__(self):
        # We're going to assume that if the object doesn't have a primary key set
        # that we failed to insert the record in the first place.
        if hasattr(self, self.pk_column):
            try:
                sql = 'DELETE FROM {} WHERE {} = {};'.format(self.table_name,
                                                             self.pk_column,
                                                             getattr(self, self.pk_column))

                self._db_cursor.execute(sql)
                self._db_connection.commit()
                self._db_cursor.close()

            except Exception as e:
                print(e)

        self._db_connection.close()

    def _insert_record(self):
        '''
        Takes a database-specific sql string as an arg.
        Inserts a new database record.
        '''
        self._db_cursor.execute(self._insert_sql_definition_string())
        self._db_connection.commit()

    def _insert_sql_definition_string(self):
        raise NotImplementedError

    def _set_primary_key_attribute(self):
        raise NotImplementedError


class MockPostgresRecord(MockRecord):

    def _insert_sql_definition_string(self):
        sql = """
            INSERT INTO {} ({})
            VALUES ({})
            RETURNING {};
        """.format(self.table_name,
                   ', '.join(self.columns),
                   ', '.join([str(getattr(self, key)) for key in self.columns]),
                   self.pk_column)

        return sql

    def _set_primary_key_attribute(self):
        '''
        Custom logic to fetch the primary key value that was just inserted
        and set it as an attribute on the object.
        The database cursor is still open from the _insert_record call.
        '''
        primary_key = self._db_cursor.fetchone()[0]
        setattr(self, self.pk_column, primary_key)


class MockMySQLRecord(MockRecord):

    def _insert_sql_definition_string(self):
        # Definitely not an ideal solution. This assumes the user is inserting a
        # record into a table with an AUTO_INCREMENT primary key column.
        sql = """
            INSERT INTO {} ({})
            VALUES ({});
        """.format(self.table_name,
                   ', '.join(self.columns),
                   ', '.join([str(getattr(self, key)) for key in self.columns]))

        return sql

    def _set_primary_key_attribute(self):
        '''
        Custom logic to fetch the primary key value that was just inserted
        and set it as an attribute on the object.
        The database cursor is still open from the _insert_record call.
        '''
        self._db_cursor.execute("SELECT LAST_INSERT_ID();")
        primary_key = self._db_cursor.fetchone()[0]
        setattr(self, self.pk_column, primary_key)


def test():
    dbargs = {
        'user': 'test',
        'password': 'test',
        'database': 'test_db',
        'host': 'localhost'
    }

    mock_rec = MockPostgresRecord(psycopg2, dbargs, 'test_table', 'test_tableid', num_val=123)

if __name__ == '__main__':
    test()
