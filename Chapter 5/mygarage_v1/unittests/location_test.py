#
# Introducing the MySQL Shell - MyGarage Version 1
#
# This file contains test cases for testing the location_test.py code module.
#
# Note: This file is intended to be run from the shell.
#
# Database name = garage_v1
#
# Dr. Charles Bell, 2019
"""Unit test for the Location class
Usage: mysqlsh --py -f unittests/location_test.py"""
from __future__ import print_function

from unittests.crud_test import CRUDTest
from database.location import Location

class LocationTests(CRUDTest):
    """Test cases for the Location class"""

    def __init__(self):
        """Constructor"""
        CRUDTest.__init__(self)
        self.location = None
        self.mygarage = None

    def set_up(self, mysql_x, user=None, passwd=None):
        """Setup the test cases"""
        self.mygarage = self.begin(mysql_x, "Location", user, passwd)
        self.location = Location(self.mygarage)

    # pylint: disable=no-self-use
    def create(self):
        """Run Create test case"""
        print("\nCRUD: Create test case (SKIPPED)")
    # pylint: enable=no-self-use

    def read_all(self):
        """Run Read(all) test case"""
        print("\nCRUD: Read (all) test case")
        rows = self.location.read()
        self.show_rows(rows, 5)

    # pylint: disable=no-self-use
    def read_one(self):
        """Run Read(record) test case"""
        print("\nCRUD: Read (row) test case (SKIPPED)")

    def update(self):
        """Run Update test case"""
        print("\nCRUD: Update test case (SKIPPED)")

    def delete(self):
        """Run Delete test case"""
        print("\nCRUD: Delete test case (SKIPPED)")
    # pylint: enable=no-self-use
