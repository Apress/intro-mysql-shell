#
# Introducing the MySQL Shell - MyGarage Version 2
#
# This file contains a class that implements a NOSQL model for the
# MyGarage application. Included are the basic functions provided for
# connecting to and disconnecting from the MySQL server.
#
# Schema name = garage_v2
#
# Dr. Charles Bell, 2019
#
""" MyGarage Database Classes Version 1"""
from __future__ import print_function

MAX_DEPTH = 10   # Maximum depth of number of drawers or shelves

# Attempt to import the mysqlx module. If unsuccessful, we are
# running from the shell and must pass mysqlx in to the class
# constructor.
try:
    import mysqlx
except Exception:
    print("Running from MySQL Shell. Provide mysqlx in constructor.")


def make_list(results, key_list):
    """Build list of Python arrays from results

    Return a Python array for the list of documents returned from a read
    operation.
    """
    result_list = []
    for result in results:
        item_values = []
        for key in key_list:
            try:
                item_values.append(result[key])
            except KeyError:
                # If key not found, create a placeholder
                item_values.append('')
        result_list.append(item_values)
    return result_list

#
# MyGarage schema simple abstraction (relational schema)
#
class MyGarage(object):
    """MyGarage master class

    Use this class to interface with the garage schema. It includes
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
        self.schema = None

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
        self.schema = self.session.get_schema('garage_v2')

    def get_session(self):
        """Return the session for use in other classes"""
        return self.session

    def get_schema(self):
        """Return the schema for use in other classes"""
        return self.schema

    def is_connected(self):
        """Check to see if connected to the server"""
        return self.session and (self.session.is_open())

    def disconnect(self):
        """Disconnect from the server"""
        try:
            self.session.close()
        except Exception as err:
            print("WARNING: {0}".format(err))

    def get_locations(self, include_organizers=True):
        """Build a list of all storage locations"""
        tool_locations = []
        # Get organizers - if selected
        if include_organizers:
            organizers = self.schema.get_collection('organizers').find().\
                fields("_id", "type", "description").execute().fetch_all()
            for organizer in organizers:
                list_item_str = "{0} - {1}".format(organizer["type"], organizer["description"])
                tool_locations.append((list_item_str, list_item_str))
        storage_collections = ['toolchests', 'shelving_units', 'workbenches', 'cabinets']
        for storage_collection in storage_collections:
            collection = self.schema.get_collection(storage_collection)
            items = collection.find().fields("_id", "description",
                                             "tool_locations").execute().fetch_all()
            for item in items:
                locations_found = item["tool_locations"]
                if locations_found:
                    for tool_loc_id in locations_found:
                        tool_location = self.schema.get_collection("locations").\
                            find('_id = :param1').bind('param1', tool_loc_id).execute().fetch_all()
                        if tool_location:
                            list_item_str = "{0}, {1} - {2}"\
                                "".format(item["description"], tool_location[0]["description"],
                                          tool_location[0]["type"])
                            tool_locations.append((list_item_str, list_item_str))
        return tool_locations

    def build_storage_contents(self, tool_locations):
        """Build the list of tools and organizers in the storage places"""
        storage_places = []
        tools = self.schema.get_collection('tools')
        organizers = self.schema.get_collection('organizers')
        locations = self.schema.get_collection('locations')
        if not tool_locations:
            return storage_places
        list_of_tools = []
        for loc_id in tool_locations:
            # Get the tool location
            tool_location = locations.find("_id = :param1").\
                bind("param1", loc_id).execute().fetch_all()
            if not tool_location or tool_location == []:
                # Check organizers
                organizer = organizers.find("_id = :param1").\
                    bind("param1", loc_id).execute().fetch_all()
                if not organizer or organizer == []:
                    continue # This is an error!
                description = organizer[0]['description']
                loc_type = organizer[0]['type']
                list_of_tools.append(('organizers', loc_type, description, 'organizer', ' '))
                continue
            else:
                try:
                    tool_id_list = tool_location[0]['tool_ids']
                except KeyError:
                    tool_id_list = []
                description = tool_location[0]['description']
                loc_type = tool_location[0]['type']
            # Now, get all of the tools
            tool_list_str = '_id in [{0}]'.format(
                ', '.join(['"{0}"'.format(t_id) for t_id in tool_id_list]))
            found_tools = tools.find(tool_list_str).execute().fetch_all()
            for tool in found_tools:
                # only some tools have a size
                size = dict(tool).get('size', ' ')
                list_of_tools.append(('tools', tool['type'], tool['description'],
                                      tool['category'], size))
            storage_places.append((loc_type, description, list_of_tools))
            list_of_tools = []
        return storage_places

    def vendor_in_use(self, vendor_id):
        """Search collections for vendor id"""
        collections = ['cabinets', 'shelving_units', 'toolchests', 'tools', 'workbenches']
        for collection_name in collections:
            collection = self.schema.get_collection(collection_name)
            res = collection.find('vendorid = :param1').\
                bind('param1', vendor_id).execute().fetch_all()
            if res:
                return True
        return False
