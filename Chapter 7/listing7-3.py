# Introducing MySQL 8 Shell
#
# Create the document store for Chapter 7 sample application 'mygarage_v2'
#
# Dr. Charles Bell
from getpass import getpass
try:
    input = raw_input
except NameError:
    pass

try:
    import mysqlx
except Exception:
    from mysqlsh import mysqlx

# Get user id and password
userid = input("User Id: ")
passwd = getpass("Password: ")

user_info = {
    'host': 'localhost',
    'port': 33060,
    'user': userid,
    'password': passwd,
}

# Connect to the database garage_v1
my_session = mysqlx.get_session(user_info)
# Create the schema for garage_v2
my_session.drop_schema('garage_v2')
garage_v2 = my_session.create_schema('garage_v2')
# Create the collections
cabinets = garage_v2.create_collection('cabinets')
organizers = garage_v2.create_collection('organizers')
shelving_units = garage_v2.create_collection('shelving_units')
tools = garage_v2.create_collection('tools')
toolchests = garage_v2.create_collection('toolchests')
locations = garage_v2.create_collection('locations')
workbenches = garage_v2.create_collection('workbenches')
vendors = garage_v2.create_collection('vendors')
# Show the collections
print(garage_v2.get_collections())