

class MockRecord(object):
	'''
	Requires a database connection object that conforms to the
	PEP-249 database API specification.

	Unpacks and inserts a database record based on the passed in kwargs.
	The initialized object contains the newly inserted primary key value.
	'''

	def __init__(self, db_connection, primary_key_column, **kwargs):
		self.db_connection = db_connection
		pass

	def __del__(self):
		pass
