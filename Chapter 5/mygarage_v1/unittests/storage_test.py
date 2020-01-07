#
# Introducing the MySQL Shell - MyGarage Version 1
#
# This file contains test cases for testing the storage_test.py code module.
#
# Note: This file is intended to be run from the shell.
#
# Database name = garage_v1
#
# Dr. Charles Bell, 2019
"""Unit test for the Storage class
Usage: mysqlsh --py -f unittests/storage_test.py"""
from __future__ import print_function

from unittests.crud_test import CRUDTest
from database.storage import Storage

class StorageTests(CRUDTest):
    """Test cases for the Storage class"""

    def __init__(self):
        """Constructor"""
        CRUDTest.__init__(self)
        self.storage = None
        self.last_id = None

    def set_up(self, mysql_x, user=None, passwd=None):
        """Setup the test cases"""
        self.mygarage = self.begin(mysql_x, "Storage", user, passwd)
        self.storage = Storage(self.mygarage)

    def create(self):
        """Run Create test case"""
        print("\nCRUD: Create test case")
        storage_data = {
            "VendorId": 101,
            "StorageType": "Shelving",
            "Description": "Loft",
            "NumDrawers": 3,
            "NumShelves": 3,
            "NumDoors": 3,
            "Width": 11,
            "Depth": 11,
            "Height": 11,
            "Location": "Ceiling",
        }
        self.storage.create(storage_data)
        self.last_id = self.mygarage.get_last_insert_id()[0]
        print("\tLast insert id = {0}".format(self.last_id))

    def read_all(self):
        """Run Read(all) test case"""
        print("\nCRUD: Read (all) test case")
        rows = self.storage.read()
        self.show_rows(rows, 5)

    def read_one(self):
        """Run Read(record) test case"""
        print("\nCRUD: Read (row) test case")
        rows = self.storage.read(self.last_id)
        print("\t{0}".format(", ".join(rows[0])))

    def update(self):
        """Run Update test case"""
        print("\nCRUD: Update test case")
        storage_data = {
            "StorageId": self.last_id,
            "VendorId": 101,
            "StorageType": "Shelving",
            "Description": "Cloud Storage",
            "NumDrawers": 2,
            "NumShelves": 4,
            "NumDoors": 6,
            "Width": 8,
            "Depth": 12,
            "Height": 14,
            "Location": "3rd floor basement",
        }
        self.storage.update(storage_data)

    def delete(self):
        """Run Delete test case"""
        print("\nCRUD: Delete test case")
        self.storage.delete(self.last_id)
        rows = self.storage.read(self.last_id)
        if not rows:
            print("\tNot found (deleted).")
