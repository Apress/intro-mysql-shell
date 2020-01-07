#
# Introducing the MySQL Shell - MyGarage Version 2
#
# This file contains test cases for testing the garage_v2.py code module.
#
# Note: This file is intended to be run from the shell.
#
# Database name = garage_v2
#
# Dr. Charles Bell, 2019
#
"""Test the garage_v2 code module"""
from __future__ import print_function

from getpass import getpass
from schema.garage_v2 import MyGarage

print("MyGarage Class Unit test")
# pylint: disable=undefined-variable
mygarage = MyGarage(mysqlx)
# pylint: enable=undefined-variable
user = raw_input("User: ")
passwd = getpass("Password: ")
print("Connecting...")
mygarage.connect(user, passwd, 'localhost', 33060)
print("Getting the schema...")
schema = mygarage.get_schema()
print(schema)
print("Getting the session...")
session = mygarage.get_session()
print(session)
print("Connected?")
print(mygarage.is_connected())
print("Disconnecting...")
mygarage.disconnect()
print("Connected?")
print(mygarage.is_connected())
