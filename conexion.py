import mysql.connector

conexion = mysql.connector.connect(
    host="189.190.30.219",
    user="Paukars",
    password="SoyPaukars",
    database="web_scrapping"
)

cursor = conexion.cursor()
cursor.execute("SHOW TABLES")

for tabla in cursor:
    print(tabla)

conexion.close()
