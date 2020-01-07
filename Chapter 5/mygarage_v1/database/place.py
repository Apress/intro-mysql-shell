#
# Introducing the MySQL Shell - MyGarage Version 1
#
# This file contains a class that implements a relational database model
# for the MyGarage application. Included are the basic create, read,
# update, and delete methods for a table in the garage_v1 database.
#
# Database name = garage_v1
# Table name = place
#
# Dr. Charles Bell, 2019
#
""" MyGarage Database Classes Version 1"""
from __future__ import print_function

#
# Constants
#
# Place
PLACE_TYPES = [('Drawer', 'Drawer'), ('Shelf', 'Shelf')]
PLACE_COLS_CREATE = ['StorageId', 'Type', 'Description', 'Width', 'Depth', 'Height']
PLACE_COLS = []
PLACE_COLS.extend(PLACE_COLS_CREATE)
PLACE_COLS.insert(0, 'Id') # Add the Id to the list
PLACE_READ_COLS = ['StorageId', 'StorageEquipment', 'LocationType', 'Location']
PLACE_READ_LIST = (
    "SELECT place.Id, storage.description as StorageEquipment, place.Type as LocationType, "
    "place.Description as Location FROM garage_v1.place JOIN "
    "garage_v1.storage ON place.StorageId = storage.ID ORDER BY "
    "StorageEquipment, LocationType, Location"
)

#
# Place table
#
class Place(object):
    """Place class

    This class encapsulates the place table permitting CRUD operations
    on the data.
    """
    def __init__(self, mygarage):
        """Constructor"""
        self.mygarage = mygarage
        self.schema = mygarage.get_db()
        self.session = mygarage.get_session()
        self.tbl = self.schema.get_table('place')

    def create(self, place_data):
        """Add a new row to the table"""
        storage_id = place_data.get("StorageId", None)
        storage_type = place_data.get("Type", None)
        description = place_data.get("Description", None)
        width = place_data.get("Width", 0)
        depth = place_data.get("Depth", 0)
        height = place_data.get("Height", 0)
        assert storage_id, "You must supply a storage Id for the place."
        assert storage_type, "You must specify a type for the place."
        assert description, "You must supply a description for the place."
        try:
            self.tbl.insert(PLACE_COLS_CREATE).values(storage_id, storage_type, description,
                                                      width, depth, height).execute()
        except Exception as err:
            print("ERROR: Cannot add place: {0}".format(err))
            return (False, err)
        return (True, None)

    def read(self, place_id=None):
        """Read data from the table"""
        try:
            if not place_id:
                # return all places - uses a JOIN so we have to use the sql()
                # method instead of select, but we arrive at the same results
                sql_res = self.session.sql(PLACE_READ_LIST).execute()
                return self.mygarage.make_rows_sql(sql_res, len(PLACE_READ_COLS))
            else:
                # return specific place
                sql_res = self.tbl.select(PLACE_COLS).where(
                    "Id = '{0}'".format(place_id)).execute()
        except Exception as err:
            print("ERROR: Cannot read place: {0}".format(err))
            return (False, err)
        return self.mygarage.make_rows(sql_res)

    def update(self, place_data):
        """Update the data for a row in the table"""
        place_id = place_data.get("PlaceId", None)
        storage_id = place_data.get("StorageId", None)
        storage_type = place_data.get("Type", None)
        description = place_data.get("Description", None)
        width = place_data.get("Width", 0)
        depth = place_data.get("Depth", 0)
        height = place_data.get("Height", 0)
        assert place_id, "You must supply an Id to update the place."
        assert storage_id, "You must supply a storage Id for the place."
        assert storage_type, "You must specify a type for the place."
        assert description, "You must supply a description for the place."
        field_value_list = [
            ('StorageId', storage_id),
            ('Type', storage_type),
            ('Description', description),
            ('Width', width),
            ('Depth', depth),
            ('Height', height)
        ]
        try:
            tbl_update = self.tbl.update()
            for field_value in field_value_list:
                tbl_update.set(field_value[0], field_value[1])
            tbl_update.where("Id = '{0}'".format(place_id)).execute()
        except Exception as err:
            print("ERROR: Cannot update place: {0}".format(err))
            return (False, err)
        return (True, None)

    def delete(self, place_id=None):
        """Delete a row from the table"""
        assert place_id, "You must supply an Id to delete the place."
        try:
            self.tbl.delete().where("Id = '{0}'".format(place_id)).execute()
        except Exception as err:
            print("ERROR: Cannot delete place: {0}".format(err))
            return (False, err)
        return (True, None)
