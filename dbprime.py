#!usr/bin python3

# ===============================================================
class MockRecord(object):
	def __init__(self, db_connection):
		self.db_connection = db_connection
		pass

	# -----------------------------------------------------------
	def __del__(self):
		pass
