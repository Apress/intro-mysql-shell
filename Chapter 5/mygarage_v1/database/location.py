#
# Introducing the MySQL Shell - MyGarage Version 1
#
# This file contains a class that implements a relational database model
# for the MyGarage application. Included are the basic create, read,
# update, and delete methods for a table in the garage_v1 database.
#
# Database name = garage_v1
# Table name = location
#
# Dr. Charles Bell, 2019
#
""" MyGarage Database Classes Version 1"""

#
# Constants
#
# Location
LOCATION_READ_COLS = ['PlaceId', 'StorageEquipment', 'Type', 'Location']
LOCATION_READ_BRIEF_COLS = ['StorageEquipment', 'Type', 'Location']

#
# Location View
#
# pylint: disable=too-few-public-methods
class Location(object):
    """Location class

    This class encapsulates the location view permitting read operations
    on the data.
    """
    def __init__(self, mygarage):
        """Constructor"""
        self.mygarage = mygarage
        self.schema = mygarage.get_db()
        self.tbl = self.schema.get_table('location')

    def read(self):
        """Read data from the table"""
        sql_res = self.tbl.select(LOCATION_READ_COLS).order_by(
            *LOCATION_READ_BRIEF_COLS).execute()
        return self.mygarage.make_rows(sql_res)
# pylint: enable=too-few-public-methods
