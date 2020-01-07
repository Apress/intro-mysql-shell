from schema.garage_v2 import MyGarage
myg = MyGarage(mysqlx)
myg.connect('root', 'SECRET', 'localhost', 33060)
schema = myg.get_schema()
s = myg.get_session()
myg.is_connected()
myg.disconnect()
myg.is_connected()
