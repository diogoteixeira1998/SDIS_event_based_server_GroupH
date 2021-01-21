import sqlite3
import sys
import time
from prettytable import PrettyTable

 

def connectDataBase( DBfile ):

    conn = sqlite3.connect(DBfile)

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


#===========================================
#  SEARCH DB with random generated data
#===========================================
def search_db(search_query, DB_name):

    #   OPEN DATA BASE CONNECTION
    start = time.time()
    connection = connectDataBase(DB_name)
    cursor = connection.cursor()
    end = time.time()
    time_connecting=(end - start)*1000
    


    #   SEARCH DATABASE FOR QUERY
    start = time.time()
    n_entries=0
    AVG_salary=0
    AVG_score= 0

    command = "SELECT * FROM personal_info WHERE Age=" + str(search_query)
    cursor.execute(command)
    output_raw = cursor.fetchall()
    if(output_raw):
        n_entries = len(output_raw)
        sum_score=0
        sum_salary=0
        print("Total entries are:  ", n_entries)
        t = PrettyTable(['ID', 'Firs name', 'Last name', 'Age', 'Salary', 'Score'])

        for column in output_raw:
            t.add_row([column[0],  column[1],    column[2],    column[3],    column[4],    column[5]]) 
            sum_salary = sum_salary + column[4]
            sum_score = sum_score + column[5]
        
        AVG_salary = sum_salary/n_entries
        AVG_score = sum_score/n_entries
        print(t) 
        print("Slaray avg:      ",  AVG_salary )
        print("Score avg:       ",  AVG_score  )
    else:
        print("No results\n")
        n_entries = 0

    end = time.time()
    time_search=(end - start)*1000
    

    #   CLOSE CONNECTION
    start = time.time()
    closeConnection(connection)
    end = time.time()
    time_closing=(end - start)*1000

    print( "Time connecting                     ", time_connecting)
    print( "Time searching                      ", time_search)
    print( "Time closing                        ", time_closing, "\n")

    search_results = [search_query, n_entries, AVG_salary, AVG_score, start]
    return search_results


#===========================================
#  INSERT INTO DB with search results
#===========================================
def history_db(results, DB_name):

    #   OPEN DATA BASE CONNECTION
    start = time.time()
    connection = connectDataBase(DB_name)
    cursor = connection.cursor()
    end = time.time()
    time_connecting2=(end - start)*1000
    

    start = time.time()
    command2 = "INSERT INTO history ( Query, Total_entries, SalaryAVG, ScoreAVG, Time) VALUES ('"+ str(results[0]) +"',"+ str(results[1]) +","+str(results[2])+","+str(results[3])+",'"+ str(results[4]) +"')"    
    cursor.execute(command2)
    connection.commit()

    
    cursor.execute("SELECT * FROM ( SELECT * FROM history ORDER BY code DESC LIMIT 5) ORDER BY code ASC")
    output_raw2 = cursor.fetchall()
    if(output_raw2):

        t = PrettyTable(['code (PK)', 'Query', 'Total_entries', 'SalaryAVG', 'ScoreAVG', 'Time'])

        for column in output_raw2:
            t.add_row([column[0],  column[1],    column[2],    column[3],    column[4],    column[5]]) 
        
        print(t) 
    else:
        print("No results\n")
    end = time.time()
    time_search2=(end - start)*1000
    

    #   CLOSE CONNECTION
    start = time.time()
    closeConnection(connection)
    end = time.time()
    time_closing2=(end - start)*1000

    print( "Time connecting to 2nd database     ", time_connecting2)
    print( "Time searching 2nd database         ", time_search2)
    print( "Time closing 2nd database           ", time_closing2)
