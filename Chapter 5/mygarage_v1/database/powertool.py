#
# Introducing the MySQL Shell - MyGarage Version 1
#
# This file contains a class that implements a relational database model
# for the MyGarage application. Included are the basic create, read,
# update, and delete methods for a table in the garage_v1 database.
#
# Database name = garage_v1
# Table name = powertool
#
# Dr. Charles Bell, 2019
#
""" MyGarage Database Classes Version 1"""
from __future__ import print_function

#
# Constants
#
# Powertool
POWERTOOL_TYPES = [('Corded', 'Corded'), ('Cordless', 'Cordless'), ('Air', 'Air')]
POWERTOOL_COLS_CREATE = ['VendorId', 'Description', 'Type', 'PlaceId']
POWERTOOL_COLS = []
POWERTOOL_COLS.extend(POWERTOOL_COLS_CREATE)
POWERTOOL_COLS.insert(0, 'Id') # Add the Id to the list
POWERTOOL_READ_COLS = [
    'Id', 'Type', 'Description', 'StorageEquipment',
    'LocationType', 'Location',
]
POWERTOOL_READ_LIST = (
    "SELECT powertool.Id, powertool.type, powertool.description, "
    "storage.description as StorageEquipment, place.type as locationtype, "
    "place.description as location FROM garage_v1.powertool JOIN garage_v1.place "
    "ON powertool.placeid = place.id JOIN garage_v1.storage ON "
    "place.storageid = storage.id ORDER BY powertool.type, powertool.description"
)

#
# Powertool table
#
class Powertool(object):
    """Powertool class

    This class encapsulates the powertool table permitting CRUD operations
    on the data.
    """
    def __init__(self, mygarage):
        """Constructor"""
        self.mygarage = mygarage
        self.schema = mygarage.get_db()
        self.session = mygarage.get_session()
        self.tbl = self.schema.get_table('powertool')

    def create(self, powertool_data):
        """Add a new row to the table"""
        vendor_id = powertool_data.get("VendorId", None)
        description = powertool_data.get("Description", None)
        tool_type = powertool_data.get("Type", None)
        place_id = powertool_data.get("PlaceId", 0)
        assert tool_type, "You must specify a type for the powertool."
        assert description, "You must supply a description for the powertool."
        assert place_id, "You must supply an Id for the powertool."
        try:
            self.tbl.insert(POWERTOOL_COLS_CREATE).values(vendor_id, description, tool_type,
                                                          place_id).execute()
        except Exception as err:
            print("ERROR: Cannot add powertool: {0}".format(err))
            return (False, err)
        return (True, None)

    def read(self, powertool_id=None):
        """Read data from the table"""
        try:
            if not powertool_id:
                # return all powertools - uses a JOIN so we have to use the sql()
                # method instead of select, but we arrive at the same results
                sql_res = self.session.sql(POWERTOOL_READ_LIST).execute()
                return self.mygarage.make_rows_sql(sql_res, len(POWERTOOL_READ_COLS))
            else:
                # return specific powertool
                sql_res = self.tbl.select(POWERTOOL_COLS).where(
                    "Id = '{0}'".format(powertool_id)).execute()
        except Exception as err:
            print("ERROR: Cannot read powertool: {0}".format(err))
            return (False, err)
        return self.mygarage.make_rows(sql_res)

    def update(self, powertool_data):
        """Update the data for a row in the table"""
        powertool_id = powertool_data.get("PowertoolId", None)
        vendor_id = powertool_data.get("VendorId", None)
        description = powertool_data.get("Description", None)
        tool_type = powertool_data.get("Type", None)
        place_id = powertool_data.get("PlaceId", 0)
        assert powertool_id, "You must supply an Id to update the powertool."
        assert tool_type, "You must specify a type for the powertool."
        assert description, "You must supply a description for the powertool."
        assert place_id, "You must supply an Id for the powertool."
        field_value_list = [
            ('VendorId', vendor_id),
            ('Description', description),
            ('Type', tool_type),
            ('PlaceId', place_id)
        ]
        try:
            tbl_update = self.tbl.update()
            for field_value in field_value_list:
                tbl_update.set(field_value[0], field_value[1])
            tbl_update.where("Id = '{0}'".format(powertool_id)).execute()
        except Exception as err:
            print("ERROR: Cannot update powertool: {0}".format(err))
            return (False, err)
        return (True, None)

    def delete(self, powertool_id=None):
        """Delete a row from the table"""
        assert powertool_id, "You must supply an Id to delete the powertool."
        try:
            self.tbl.delete().where("Id = '{0}'".format(powertool_id)).execute()
        except Exception as err:
            print("ERROR: Cannot delete powertool: {0}".format(err))
            return (False, err)
        return (True, None)
