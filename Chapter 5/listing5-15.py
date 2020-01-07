from database.garage_v1 import MyGarage
LOCATION_READ_COLS = ['PlaceId', 'StorageEquipment', 'Type', 'Location']
LOCATION_READ_BRIEF_COLS = ['StorageEquipment', 'Type', 'Location']
class Location(object):
    def __init__(self, myg):
        self.table = myg.get_db().get_table('location')
    
    def read(self):
        sql_res = self.table.select(LOCATION_READ_COLS).order_by(*LOCATION_READ_BRIEF_COLS).limit(5).execute()
        return(mygarage.make_rows(sql_res))

mygarage = MyGarage(mysqlx)
mygarage.connect('root', 'SECRET', 'localhost', 33060)
location = Location(mygarage)
rows = location.read()
print(rows)
    
    