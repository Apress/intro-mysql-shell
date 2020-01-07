#
# Introducing MySQL Shell
#
# This example shows how to use the MySQL Router to connect to
# the cluster. Notice how connecting via the router port 6446
# results in a seamless transport to one of the cluster servers,
# in this case, the server with the primary role.
#
# Dr. Charles Bell, 2019
# 
import mysql.connector

# Simple function to display results from a cursor
def show_results(cur_obj):
  for row in cur:
    print(row)

my_cfg = {
  'user':'root',
  'passwd':'secret',
  'host':'127.0.0.1',
  'port':6446   # <<<< Router port (R/W)
}

# Connecting to the server
conn = mysql.connector.connect(**my_cfg)

print("Listing the databases on the server.")
query = "SHOW DATABASES"
cur = conn.cursor()
cur.execute(query)
show_results(cur)

print("\nRetrieve the port for the server to which we're connecting.")
query = "SELECT @@port"
cur = conn.cursor()
cur.execute(query)
show_results(cur)

# Close the cursor and connection
cur.close()
conn.close()
