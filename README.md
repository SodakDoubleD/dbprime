# dbprime
### Used to create temporary mocked database records for integration testing.

#### How it works:
* Hand the MockRecord constructor a PEP-249 compliant python database module, database args to connect with, a table name, a primary key column, and any other key/value pairs that you wish to fill in the mocked database record
* Each MockRecord object creates and manages its own database connection
* A new database record is inserted and the primary key value is then set as an attribute on the object
* Upon garbage collection or deletion, the object deletes the record it inserted into the database and then closes its connection. Completely hands-off for the user.

#### What it's good for:
* Creation/deletion of simple database records to be used in unit tests
* Legitimate end-to-end query verification: insert a basic record and ensure that your query runs without error
* Testing the relationship between the database and the python code that queries it
* Best part: **_no dependencies_**. The dbprime module is completely self-contained.

#### What it's not good for:
* Creating a bunch of complex database records. It can be done, but it's not pretty
* In the case of tables that reference other tables, you have to create the FK object first and then supply the linked value from that object to the secondarily-created object that references it. Not ideal.
