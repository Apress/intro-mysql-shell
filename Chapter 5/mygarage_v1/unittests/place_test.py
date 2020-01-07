#
# Introducing the MySQL Shell - MyGarage Version 1
#
# This file contains test cases for testing the place_test.py code module.
#
# Note: This file is intended to be run from the shell.
#
# Database name = garage_v1
#
# Dr. Charles Bell, 2019
"""Unit test for the Place class
Usage: mysqlsh --py -f unittests/place_test.py"""
from __future__ import print_function

from unittests.crud_test import CRUDTest
from database.place import Place

class PlaceTests(CRUDTest):
    """Test cases for the Place class"""

    def __init__(self):
        """Constructor"""
        CRUDTest.__init__(self)
        self.place = None
        self.last_id = None

    def set_up(self, mysql_x, user=None, passwd=None):
        """Setup the test cases"""
        self.mygarage = self.begin(mysql_x, "Place", user, passwd)
        self.place = Place(self.mygarage)

    def create(self):
        """Run Create test case"""
        print("\nCRUD: Create test case")
        place_data = {
            "StorageId": 201,
            "Type": "Drawer",
            "Description": 'Blackhole',
            "Width": 0,
            "Depth": 0,
            "Height": 0,
        }
        self.place.create(place_data)
        self.last_id = self.mygarage.get_last_insert_id()[0]
        print("\tLast insert id = {0}".format(self.last_id))

    def read_all(self):
        """Run Read(all) test case"""
        print("\nCRUD: Read (all) test case")
        rows = self.place.read()
        self.show_rows(rows, 5)

    def read_one(self):
        """Run Read(record) test case"""
        print("\nCRUD: Read (row) test case")
        rows = self.place.read(self.last_id)
        print("\t{0}".format(", ".join(rows[0])))

    def update(self):
        """Run Update test case"""
        print("\nCRUD: Update test case")
        place_data = {
            "PlaceId": self.last_id,
            "StorageId": 201,
            "Type": "Drawer",
            "Description": 'Junk drawer',
            "Width": 24,
            "Depth": 12,
            "Height": 4,
        }
        self.place.update(place_data)

    def delete(self):
        """Run Delete test case"""
        print("\nCRUD: Delete test case")
        self.place.delete(self.last_id)
        rows = self.place.read(self.last_id)
        if not rows:
            print("\tNot found (deleted).")
