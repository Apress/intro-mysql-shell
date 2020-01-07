#
# Introducing the MySQL Shell - MyGarage Version 1
#
# This file contains a class that implements a relational database model
# for the MyGarage application. Included are the basic functions provided for
# connecting to and disconnecting from the MySQL server.
#
# Database name = garage_v1
#
# Dr. Charles Bell, 2019
#
""" MyGarage Database Classes Version 1"""
from __future__ import print_function

# Attempt to import the mysqlx module. If unsuccessful, we are
# running from the shell and must pass mysqlx in to the class
# constructor.
try:
    import mysqlx
except Exception:
    print("Running from MySQL Shell. Provide mysqlx in constructor.")

#
# MyGarage database simple abstraction (relational database)
#
class MyGarage(object):
    """MyGarage master class

    Use this class to interface with the garage database. It includes
    utility functions for connections to the server as well as running
    queries.
    """
    def __init__(self, mysqlx_sh=None):
        self.session = None
        if mysqlx_sh:
            self.mysqlx = mysqlx_sh
            self.using_shell = True
        else:
            self.mysqlx = mysqlx
            self.using_shell = False

    def connect(self, username, passwd, host, port):
        """Connect to a MySQL server at host, port

        Attempts to connect to the server as specified by the connection
        parameters.
        """
        config = {
            'user': username,
            'password': passwd,
            'host': host,
            'port': port,
        }
        try:
            self.session = self.mysqlx.get_session(**config)
        except Exception as err:
            print("CONNECTION ERROR:", err)
            self.session = None
            raise

    def get_session(self):
        """Return the session for use in other classes"""
        return self.session

    def get_db(self):
        """Return the database for use in other classes"""
        return self.session.get_schema('garage_v1')

    def is_connected(self):
        """Check to see if connected to the server"""
        return self.session and (self.session.is_open())

    def disconnect(self):
        """Disconnect from the server"""
        try:
            self.session.close()
        except Exception as err:
            print("WARNING: {0}".format(err))

    def make_rows(self, sql_select):
        """Build row array

        Return a Python array for the rows returned from a read operation
        from a select result.
        """
        cols = []
        if self.using_shell:
            cols = sql_select.get_column_names()
        else:
            for col in sql_select.columns:
                cols.append(col.get_column_name())
        rows = []
        for row in sql_select.fetch_all():
            row_item = []
            for col in cols:
                if self.using_shell:
                    # Note: you can also use rows[cols.index(col)]
                    row_item.append("{0}".format(row.get_field(col)))
                else:
                    row_item.append("{0}".format(row[col]))
            rows.append(row_item)
        return rows

    @staticmethod
    def make_rows_sql(sql_res, num_cols):
        """Build row array

        Return a Python array for the rows returned from a read operation
        from a sql result.
        """
        rows = []
        all_rows = sql_res.fetch_all()
        for row in all_rows:
            row_item = []
            for col in range(0, num_cols):
                row_item.append("{0}".format(row[col]))
            rows.append(row_item)
        return rows

    def get_last_insert_id(self):
        """Get the last insert id"""
        return self.get_session().sql("SELECT LAST_INSERT_ID()").execute().fetch_one()
