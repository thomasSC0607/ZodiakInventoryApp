import mysql.connector 

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'madagascar12'
)

# Prepare a cursor object 
cursorObject = dataBase.cursor()

# Create the database
cursorObject.execute("CREATE DATABASE zodiak_inventory_db")

print("All Done!!!")