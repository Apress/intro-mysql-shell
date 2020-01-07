#
# Introducing the MySQL Shell - MyGarage Version 1
#
# This file contains a class that implements a relational database model
# for the MyGarage application. Included are the basic create, read,
# update, and delete methods for a table in the garage_v1 database.
#
# Database name = garage_v1
# Table name = handtool
#
# Dr. Charles Bell, 2019
#
""" MyGarage Database Classes Version 1"""
from __future__ import print_function

#
# Constants
#
# Handtool
HANDTOOL_TYPES = [
    ('Adjustable Wrench', 'Adjustable Wrench'), ('Awl', 'Awl'),
    ('Clamp', 'Clamp'), ('Crowbar', 'Crowbar'), ('Drill Bit', 'Drill Bit'),
    ('File', 'File'), ('Hammer', 'Hammer'), ('Knife', 'Knife'), ('Level', 'Level'),
    ('Nutdriver', 'Nutdriver'), ('Pliers', 'Pliers'), ('Prybar', 'Prybar'),
    ('Router Bit', 'Router Bit'), ('Ruler', 'Ruler'), ('Saw', 'Saw'),
    ('Screwdriver', 'Screwdriver'), ('Socket', 'Socket'),
    ('Socket Wrench', 'Socket Wrench'), ('Wrench', 'Wrench'),
]
HANDTOOL_COLS_CREATE = [
    'VendorId', 'Description', 'Type', 'ToolSize', 'PlaceId',
]
HANDTOOL_COLS = []
HANDTOOL_COLS.extend(HANDTOOL_COLS_CREATE)
HANDTOOL_COLS.insert(0, 'Id') # Add the Id to the list
HANDTOOL_READ_COLS = [
    'Id', 'ToolType', 'Description', 'Tool Size/Application', 'StorageEquipment',
    'LocationType', 'Location',
]
HANDTOOL_READ_LIST = (
    "SELECT handtool.Id, handtool.type, handtool.description, "
    "handtool.toolsize, storage.description as StorageEquipment, "
    "place.type as locationtype, place.description as location FROM garage_v1.handtool "
    "JOIN garage_v1.place ON "
    "handtool.placeid = place.id JOIN garage_v1.storage ON place.storageid = storage.id "
    "ORDER BY handtool.type, handtool.description"
)

#
# Handtool table
#
class Handtool(object):
    """Handtool class

    This class encapsulates the handtool table permitting CRUD operations
    on the data.
    """
    def __init__(self, mygarage):
        """Constructor"""
        self.mygarage = mygarage
        self.schema = mygarage.get_db()
        self.session = mygarage.get_session()
        self.tbl = self.schema.get_table('handtool')

    def create(self, handtool_data):
        """Add a new row to the table"""
        vendor_id = handtool_data.get("VendorId", None)
        description = handtool_data.get("Description", None)
        handtool_type = handtool_data.get("Type", None)
        tool_size = handtool_data.get("ToolSize", None)
        place_id = handtool_data.get("PlaceId", 0)
        assert tool_size, "You must specify a toolsize for the handtool."
        assert handtool_type, "You must specify a type for the handtool."
        assert description, "You must supply a description for the handtool."
        assert place_id, "You must supply an Id for the handtool."
        try:
            self.tbl.insert(HANDTOOL_COLS_CREATE).values(vendor_id, description, handtool_type,
                                                         tool_size, place_id).execute()
        except Exception as err:
            print("ERROR: Cannot add handtool: {0}".format(err))
            return (False, err)
        return (True, None)

    def read(self, handtool_id=None):
        """Read data from the table"""
        try:
            if not handtool_id:
                # return all handtools - uses a JOIN so we have to use the sql()
                # method instead of select, but we arrive at the same results
                sql_res = self.session.sql(HANDTOOL_READ_LIST).execute()
                return self.mygarage.make_rows_sql(sql_res, len(HANDTOOL_READ_COLS))
            else:
                # return specific handtool
                sql_res = self.tbl.select(HANDTOOL_COLS).where(
                    "Id = '{0}'".format(handtool_id)).execute()
        except Exception as err:
            print("ERROR: Cannot read handtool: {0}".format(err))
            return (False, err)
        return self.mygarage.make_rows(sql_res)

    def update(self, handtool_data):
        """Update the data for a row in the table"""
        handtool_id = handtool_data.get('HandtoolId', None)
        vendor_id = handtool_data.get("VendorId", None)
        description = handtool_data.get("Description", None)
        handtool_type = handtool_data.get("Type", None)
        tool_size = handtool_data.get("ToolSize", None)
        place_id = handtool_data.get("PlaceId", 0)
        assert handtool_id, "You must supply an Id to update the handtool."
        assert tool_size, "You must specify a toolsize for the handtool."
        assert handtool_type, "You must specify a type for the handtool."
        assert description, "You must supply a description for the handtool."
        assert place_id, "You must supply an Id for the handtool."
        field_value_list = [
            ('VendorId', vendor_id),
            ('Description', description),
            ('Type', handtool_type),
            ('Toolsize', tool_size),
            ('PlaceId', place_id)
        ]
        try:
            tbl_update = self.tbl.update()
            for field_value in field_value_list:
                tbl_update.set(field_value[0], field_value[1])
            tbl_update.where("Id = '{0}'".format(handtool_id)).execute()
        except Exception as err:
            print("ERROR: Cannot update handtool: {0}".format(err))
            return (False, err)
        return (True, None)

    def delete(self, handtool_id=None):
        """Delete a row from the table"""
        assert handtool_id, "You must supply an Id to delete the handtool."
        try:
            self.tbl.delete().where("Id = '{0}'".format(handtool_id)).execute()
        except Exception as err:
            print("ERROR: Cannot delete handtool: {0}".format(err))
            return (False, err)
        return (True, None)
