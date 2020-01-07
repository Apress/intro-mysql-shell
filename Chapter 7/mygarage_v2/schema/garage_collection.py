#
# Introducing the MySQL Shell - MyGarage Version 2
#
# This file contains a base class that implements a NOSQL model for the
# MyGarage application. Included are the basic create, read, update,
# and delete methods for a table in the garage_v2 schema.
#
# Use this class to define collection specific classes that include
# code for controlling behaviour specific to the collection such as required
# fields, validation, etc.
#
# Database name = garage_v2
#
# Dr. Charles Bell, 2019
#
""" MyGarage Database Classes Version 1"""
from __future__ import print_function

#
# Base garage collection
#
class GarageCollection(object):
    """GarageCollection base class

    This class encapsulates a collection permitting CRUD operations on the document.
    Use this class to define a new class adding in the required field checks specific
    to the collection.
    """
    def __init__(self, mygarage, collection_name):
        """Constructor"""
        self.mygarage = mygarage
        self.schema = mygarage.get_schema()
        self.collection_name = collection_name
        self.col = self.schema.get_collection(collection_name)
        self.docid = None

    # pylint: disable=unused-argument, no-self-use
    def check_create_prerequisites(self, doc_data):
        """Check prerequisites for the create operation.

        Note: you must complete this method in the derived class.
        """
        return True

    def check_update_prerequisites(self, doc_data):
        """Check prerequisites for the update operation.

        Note: you must complete this method in the derived class.
        """
        return True
    # pylint: enable=unused-argument, no-self-use

    def create(self, doc_data):
        """Add a new document to the collection"""
        # Validate required fields
        if not self.check_create_prerequisites(doc_data):
            return (False, "Required fields missing.")
        try:
            json_str = {}
            # Build JSON document for keys present in the dictionary
            for key in doc_data.keys():
                json_str.update({key: doc_data[key]})
            self.docid = self.col.add(json_str).execute().get_generated_ids()[0]
        except Exception as err:
            print("ERROR: Cannot add {0}: {1}".format(err, self.collection_name))
            return (False, err)
        return (True, None)

    def read(self, _id=None):
        """Read data from the collection"""
        if not _id:
            # return all documents
            res = self.col.find().execute().fetch_all()
        else:
            # return specific document
            res = self.col.find('_id = :param1').bind('param1', _id).execute().fetch_all()
        return res

    def update(self, doc_data):
        """Update the data for a document in the collection"""
        _id = doc_data.get("_id", None)
        assert _id, "You must supply an Id to update the {0}."\
            "".format(self.collection_name.rstrip('s'))
        # Validate required fields
        if not self.check_update_prerequisites(doc_data):
            return (False, "Required fields missing.")
        try:
            # Update values for keys present in the document
            for key in doc_data.keys():
                # Skip the _id key
                if key != '_id':
                    self.col.modify('_id = :param1') \
                        .bind('param1', _id) \
                        .set(key, doc_data[key]).execute()
        except Exception as err:
            print("ERROR: Cannot update {0}: {1}".format(
                self.collection_name.rstrip('s'), err))
            return (False, err)
        return (True, None)

    def delete(self, _id=None):
        """Delete a document from the collection"""
        assert _id, "You must supply an Id to delete the {0}."\
            "".format(self.collection_name.rstrip('s'))
        try:
            self.col.remove('_id = :param1').bind('param1', _id).execute()
        except Exception as err:
            print("ERROR: Cannot delete {0}: {1}".format(self.collection_name.rstrip('s'), err))
            return (False, err)
        return (True, None)

    def get_last_docid(self):
        """Get the last document id"""
        docid = self.docid
        self.docid = None # Clear it after it was read
        return docid

    def get_tool_locations(self, _id=None):
        """Get the list of tool locations (tool locations)"""
        assert _id, "You must supply an Id to get the tool locations."
        results = []
        if _id:
            places = self.col.find('_id = :param1').bind('param1', _id).\
                fields("tool_locations").execute().fetch_all()
            try:
                tool_locations = places[0]["tool_locations"]
                if tool_locations:
                    # Avoid a circular reference by getting the collection and reading directly
                    locations = self.mygarage.get_schema().get_collection("locations")
                    tool_ids = ', '.join(['"{0}"'.format(tool_id) for tool_id in tool_locations])
                    tool_loc_str = '_id in [{0}]'.format(tool_ids)
                    results = locations.find(tool_loc_str).execute().fetch_all()
            except KeyError:
                results = []
        return results
