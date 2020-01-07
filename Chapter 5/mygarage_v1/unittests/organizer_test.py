#
# Introducing the MySQL Shell - MyGarage Version 1
#
# This file contains test cases for testing the organizer_test.py code module.
#
# Note: This file is intended to be run from the shell.
#
# Database name = garage_v1
#
# Dr. Charles Bell, 2019
"""Unit test for the Organizer class
Usage: mysqlsh --py -f unittests/organizer_test.py"""
from __future__ import print_function

from unittests.crud_test import CRUDTest
from database.organizer import Organizer

class OrganizerTests(CRUDTest):
    """Test cases for the Organizer class"""

    def __init__(self):
        """Constructor"""
        CRUDTest.__init__(self)
        self.organizer = None
        self.last_id = None

    def set_up(self, mysql_x, user=None, passwd=None):
        """Setup the test cases"""
        self.mygarage = self.begin(mysql_x, "Organizer", user, passwd)
        self.organizer = Organizer(self.mygarage)

    def create(self):
        """Run Create test case"""
        print("\nCRUD: Create test case")
        organizer_data = {
            "PlaceId": 1001,
            "Type": 'Case',
            "Description": 'Nut bucket',
            "Width": 9,
            "Depth": 3,
            "Height": 2,
        }
        self.organizer.create(organizer_data)
        self.last_id = self.mygarage.get_last_insert_id()[0]
        print("\tLast insert id = {0}".format(self.last_id))

    def read_all(self):
        """Read test case"""
        print("\nCRUD: Read (all) test case")
        rows = self.organizer.read()
        self.show_rows(rows, 5)

    def read_one(self):
        """Run Read(record) test case"""
        print("\nCRUD: Read (row) test case")
        rows = self.organizer.read(self.last_id)
        print("\t{0}".format(", ".join(rows[0])))

    def update(self):
        """Run Update test case"""
        print("\nCRUD: Update test case")
        organizer_data = {
            "OrganizerId": self.last_id,
            "PlaceId": 1001,
            "Type": 'Case',
            "Description": 'Jewelry Tray',
            "Width": 3,
            "Depth": 4,
            "Height": 5,
        }
        self.organizer.update(organizer_data)

    def delete(self):
        """Run Delete test case"""
        print("\nCRUD: Delete test case")
        self.organizer.delete(self.last_id)
        rows = self.organizer.read(self.last_id)
        if not rows:
            print("\tNot found (deleted).")
