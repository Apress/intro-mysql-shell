from database.garage_v1 import MyGarage
from database.location import Location
mygarage = MyGarage(mysqlx)
mygarage.connect('root', 'SECRET', 'localhost', 33060)
location = Location(mygarage)
rows = location.read()
print(rows[:5])
