from database.garage_v1 import MyGarage
LOCATION_READ_COLS = ['PlaceId', 'StorageEquipment', 'Type', 'Location']
LOCATION_READ_BRIEF_COLS = ['StorageEquipment', 'Type', 'Location']
mygarage = MyGarage(mysqlx)
mygarage.connect('root', 'SECRET', 'localhost', 33060)
schema = mygarage.get_db()
table = schema.get_table('location')
sql_res = table.select(LOCATION_READ_COLS).order_by(*LOCATION_READ_BRIEF_COLS).limit(5).execute()
rows = mygarage.make_rows(sql_res)
print(rows)
    
    