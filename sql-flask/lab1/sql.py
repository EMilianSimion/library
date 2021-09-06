import sys

import mysql.connector


def insert(id, autor, titlu, gen, an, editor, rezumat):
    mySql_insert_query = f"""INSERT INTO carti (id, autor, titlu, gen, an, editor, rezumat) 
                             VALUES 
                             ({id}, '{autor}', '{titlu}', '{gen}', {an}, '{editor}', '{rezumat}') """
    id = id + 1
    return mySql_insert_query


def select():
    mySql_select_query = """SELECT * from carti"""
    return mySql_select_query


def create_user(name, passo):
    mySql_create_query = f"""CREATE USER '{name}'@'localhost' IDENTIFIED BY '{passo}';"""
    return mySql_create_query


def delete_user(name):
    mySql_delete_query = f"""DROP USER'{name}'@'localhost';"""
    return mySql_delete_query


def delete_book(id):
    mySql_deleteb_query = f"""DELETE FROM carti WHERE id = {id};"""
    return mySql_deleteb_query


def menu():
    print("1 -> Insert new books\n"
          "2 -> Show all books\n"
          "3-> Delete book by id\n"
          "4 -> Update book by id\n"
          "5 -> Create new user\n"
          "6 -> Delete user")


user = input("user: ")
password = input("password: ")

try:
    mydb = mysql.connector.connect(
        host="localhost",
        user=user,
        password=password,
        database="biblioteca"
    )
    menu()
    alegere = input()
    queri = ""
    mycursor = mydb.cursor()
    if alegere == '1':
        id = 0
        autor = input("autor ")
        titlu = input("titlu ")
        gen = input("gen ")
        an = input("an ")
        editor = input("editor ")
        rezumat = input("rezumat ")
        mycursor.execute("SELECT max(id) from carti;")
        records = mycursor.fetchall()
        for row in records:
            id = row[0]
            print(f"id ul este {id}")

        queri = insert(id + 1, autor, titlu, gen, an, editor, rezumat)

        mycursor.execute(queri)
        mydb.commit()

    elif alegere == '2':
        mycursor.execute(select())
        records = mycursor.fetchall()
        print("\nPrinting each book record")
        for row in records:
            print("Id = ", row[0], )
            print("Autor = ", row[1])
            print("Titlu  = ", row[2])
            print("Gen  = ", row[3])
            print("An  = ", row[4])
            print("Editor  = ", row[5])
            print("Rezumat  = ", row[6], "\n")
    elif alegere == '3':
        idd = input("book to delete by id: ")
        mycursor.execute(delete_book(idd))
        mydb.commit()

    elif alegere == '5':
        name = input("name: ")
        passw = input("password: ")
        mycursor.execute(create_user(name, passw))
        # mydb.commit()

except mysql.connector.Error as error:
    print("Eroare: " + str(error))
    sys.exit(1)
finally:
    if (mydb.is_connected()):
        mydb.close()
        mycursor.close()
        print("MySQL connection is closed")
