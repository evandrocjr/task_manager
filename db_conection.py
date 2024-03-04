import mysql.connector

# Database conection

# check if a database exists and create if not
def check_and_create_database():
    db = mysql.connector.connect(
        host="localhost",
        user="eva",
        password="zxcasdqwe123"
    )
    mycursor = db.cursor()
    
    mycursor.execute("SHOW DATABASES")
    databases = mycursor.fetchall()
    for database in databases:
        if database[0] == "gerenciador_tarefas":
            return True
    # If the database does not exist, create it
    mycursor.execute("CREATE DATABASE gerenciador_tarefas")
    return False

check_and_create_database()