import sqlite3
import sys

 

def connectDataBase( DBfile ):
    # define conn 
    conn = sqlite3.connect(DBfile)
    # ver se está no modo de multi threads
    if(conn):
        print("\n -----> Connected to: ", DBfile, "\n")
    return conn

def closeConnection(conn):
    if (conn):
        conn.close()
        print(" -----> The Sqlite connection is closed \n\n")
    else:
        print("No connection to close")


########################################################################################


def main():

    #   GET SEARCH QUERY 
    print("Search for:")       
    search_query = input()

    #   OPEN DATA BASE CONNECTION
    connection = connectDataBase('TEST_DB.db')
    cursor = connection.cursor()


    #   SEARCH DATABASE FOR QUERY
    command = "SELECT * FROM names WHERE NAME='" + search_query + "'"
    cursor.execute(command)
    output_raw = cursor.fetchall()
    if(output_raw):
        print(output_raw, "\n\n")
        print("Total columns are:  ", len(output_raw))
        for column in output_raw:
            print("ID:      ", column[0])
            print("NAME:    ", column[1])
            print("\n")
    else:
        print("No results\n")

    command2 = "SELECT * FROM grades WHERE ID=" + str(column[0]) 
    print(command2)
    cursor.execute(command2)
    output_raw = cursor.fetchall()
    if(output_raw):
        print(output_raw, "\n\n")
        print("Total columns are:  ", len(output_raw))
        for column in output_raw:
            print("Grade_ID:    ", column[0])
            print("Grade:       ", column[1])
            print("personal ID: ", column[2])
            print("\n")
    else:
        print("No results\n")

    #   CLOSE CONNECTION
    closeConnection(connection)

main()


"""
# create table

    create_names = "" CREATE TABLE IF NOT EXISTS
    names(ID INT PRIMARY KEY NOT NULL, NAME TEXT) ""

    cursor.execute(create_names)

    #cursor.execute("INSERT INTO names VALUES(2, 'Ines') ")

    connection.commit()

    # get data
    cursor.execute("SELECT * FROM names")


    names = cursor.fetchall()
    print(names)

"""