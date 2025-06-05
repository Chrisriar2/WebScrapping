import mysql.connector

conexion = mysql.connector.connect(
    host="", #insert your server's IP
    user="", #select a database's user
    password=" ",
    database="web_scrapping"
)

cursor = conexion.cursor()
cursor.execute("SHOW TABLES")

for tabla in cursor:
    print(tabla)

conexion.close()
