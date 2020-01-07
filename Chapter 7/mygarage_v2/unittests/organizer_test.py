#
# Introducing the MySQL Shell - MyGarage Version 2
#
# This file contains test cases for testing the organizer_test.py code module.
#
# Note: This file is intended to be run from the shell.
#
# Database name = garage_v2
#
# Dr. Charles Bell, 2019
"""Unit test for the Organizers class
Usage: mysqlsh --py -f unittests/organizer_test.py"""
from __future__ import print_function

from unittests.crud_test import CRUDTest
from schema.organizers import Organizers

class OrganizerTests(CRUDTest):
    """Test cases for the Organizer class"""

    def __init__(self):
        """Constructor"""
        CRUDTest.__init__(self)
        self.organizer = None
        self.last_id = None
        self.organizers = None

    def set_up(self, mysql_x, user=None, passwd=None):
        """Setup the test cases"""
        self.mygarage = self.begin(mysql_x, "Organizers", user, passwd)
        self.organizers = Organizers(self.mygarage)

    def create(self):
        """Run Create test case"""
        print("\nCRUD: Create test case")
        organizer_data = {
            "description": "SAE Socket Set",
            "tool_ids": [
                "00005cb1065c000000000000021a",
                "00005cb1065c000000000000021b",
                "00005cb1065c000000000000021c",
                "00005cb1065c000000000000021d",
                "00005cb1065c000000000000021e",
            ],
            "type": "Case",
            "height": 4,
            "width": 5,
            "depth": 12,
        }
        self.organizers.create(organizer_data)
        self.last_id = self.organizers.get_last_docid()
        print("\tLast insert id = {0}".format(self.last_id))

    def read_all(self):
        """Run Read(all) test case"""
        print("\nCRUD: Read (all) test case")
        docs = self.organizers.read()
        self.show_docs(docs, 5)

    def read_one(self):
        """Run Read(record) test case"""
        print("\nCRUD: Read (doc) test case")
        docs = self.organizers.read(self.last_id)
        self.show_docs(docs, 1)

    def update(self):
        """Run Update test case"""
        print("\nCRUD: Update test case")
        organizer_data = {
            "_id": self.last_id,
            "tool_ids": [
                "00005cb1065c000000000000021c",
                "00005cb1065c000000000000021d",
                "00005cb1065c000000000000021e",
            ],
        }
        self.organizers.update(organizer_data)

    def delete(self):
        """Run Delete test case"""
        print("\nCRUD: Delete test case")
        self.organizers.delete(self.last_id)
        docs = self.organizers.read(self.last_id)
        if not docs:
            print("\tNot found (deleted).")
