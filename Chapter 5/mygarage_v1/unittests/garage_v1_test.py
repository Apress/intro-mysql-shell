#
# Introducing the MySQL Shell - MyGarage Version 1
#
# This file contains test cases for testing the garage_v1.py code module.
#
# Note: This file is intended to be run from the shell.
#
# Database name = garage_v1
#
# Dr. Charles Bell, 2019
#
"""Test the garage_v1 code module"""
from __future__ import print_function

from getpass import getpass
from database.garage_v1 import MyGarage

print("MyGarage Class Unit test")
# pylint: disable=undefined-variable
mygarage = MyGarage(mysqlx)
# pylint: enable=undefined-variable
user = raw_input("User: ")
passwd = getpass("Password: ")
print("Connecting...")
mygarage.connect(user, passwd, 'localhost', 33060)
print("Getting the database...")
database = mygarage.get_db()
print(database)
print("Getting the session...")
session = mygarage.get_session()
print(session)
print("Connected?")
print(mygarage.is_connected())
print("Disconnecting...")
mygarage.disconnect()
print("Connected?")
print(mygarage.is_connected())
