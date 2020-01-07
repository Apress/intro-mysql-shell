#
# Introducing the MySQL Shell - MyGarage Version 1
#
# This file contains a class that implements a relational database model
# for the MyGarage application. Included are the basic create, read,
# update, and delete methods for a table in the garage_v1 database.
#
# Database name = garage_v1
# Table name = organizer
#
# Dr. Charles Bell, 2019
#
""" MyGarage Database Classes Version 1"""
from __future__ import print_function

#
# Constants
#
# Organizer
ORGANIZER_TYPES = [('Bin', 'Bin'), ('Box', 'Box'), ('Case', 'Case')]
ORGANIZER_COLS_CREATE = ['PlaceId', 'Type', 'Description', 'Width', 'Depth', 'Height']
ORGANIZER_COLS = []
ORGANIZER_COLS.extend(ORGANIZER_COLS_CREATE)
ORGANIZER_COLS.insert(0, 'Id') # Add the Id to the list
ORGANIZER_READ_COLS = [
    'Id', 'Type', 'Description', 'StorageEquipment', 'LocationType', 'Location',
]
ORGANIZER_READ_LIST = (
    "SELECT organizer.Id, organizer.Type, organizer.Description, "
    "storage.description as StorageEquipment, place.type as LocationType, "
    "place.description as Location FROM  garage_v1.organizer JOIN "
    "garage_v1.place ON organizer.placeid = place.ID  JOIN "
    "garage_v1.storage ON place.storageid = storage.id "
    "ORDER BY Type, organizer.description"
)

#
# Organizer table
#
class Organizer(object):
    """Organizer class

    This class encapsulates the organizer table permitting CRUD operations
    on the data.
    """
    def __init__(self, mygarage):
        """Constructor"""
        self.mygarage = mygarage
        self.schema = mygarage.get_db()
        self.session = mygarage.get_session()
        self.tbl = self.schema.get_table('organizer')

    def create(self, organizer_data):
        """Add a new row to the table"""
        place_id = organizer_data.get("PlaceId", None)
        organizer_type = organizer_data.get("Type", None)
        description = organizer_data.get("Description", None)
        width = organizer_data.get("Width", 0)
        depth = organizer_data.get("Depth", 0)
        height = organizer_data.get("Height", 0)
        assert place_id, "You must supply a place Id for the organizer."
        assert organizer_type, "You must specify a type for the organizer."
        assert description, "You must supply a description for the organizer."
        try:
            self.tbl.insert(ORGANIZER_COLS_CREATE).values(place_id, organizer_type, description,
                                                          width, depth, height).execute()
        except Exception as err:
            print("ERROR: Cannot add organizer: {0}".format(err))
            return (False, err)
        return (True, None)

    def read(self, organizer_id=None):
        """Read data from the table"""
        try:
            if not organizer_id:
                # return all organizers - uses a JOIN so we have to use the sql()
                # method instead of select, but we arrive at the same results
                sql_res = self.session.sql(ORGANIZER_READ_LIST).execute()
                return self.mygarage.make_rows_sql(sql_res, len(ORGANIZER_READ_COLS))
            else:
                # return specific organizer
                sql_res = self.tbl.select(ORGANIZER_COLS).where(
                    "Id = '{0}'".format(organizer_id)).execute()
        except Exception as err:
            print("ERROR: Cannot read organizer: {0}".format(err))
            return (False, err)
        return self.mygarage.make_rows(sql_res)

    def update(self, organizer_data):
        """Update the data for a row in the table"""
        organizer_id = organizer_data.get("OrganizerId", None)
        place_id = organizer_data.get("PlaceId", None)
        organizer_type = organizer_data.get("Type", None)
        description = organizer_data.get("Description", None)
        width = organizer_data.get("Width", 0)
        depth = organizer_data.get("Depth", 0)
        height = organizer_data.get("Height", 0)
        assert organizer_id, "You must supply an Id to update the organizer."
        assert place_id, "You must supply a place Id for the organizer."
        assert organizer_type, "You must specify a type for the organizer."
        assert description, "You must supply a description for the organizer."
        field_value_list = [
            ('PlaceId', place_id),
            ('Type', organizer_type),
            ('Description', description),
            ('Width', width),
            ('Depth', depth),
            ('Height', height)
        ]
        try:
            tbl_update = self.tbl.update()
            for field_value in field_value_list:
                tbl_update.set(field_value[0], field_value[1])
            tbl_update.where("Id = '{0}'".format(organizer_id)).execute()
        except Exception as err:
            print("ERROR: Cannot update organizer: {0}".format(err))
            return (False, err)
        return (True, None)

    def delete(self, organizer_id=None):
        """Delete a row from the table"""
        assert organizer_id, "You must supply an Id to delete the organizer."
        try:
            self.tbl.delete().where("Id = '{0}'".format(organizer_id)).execute()
        except Exception as err:
            print("ERROR: Cannot delete organizer: {0}".format(err))
            return (False, err)
        return (True, None)
