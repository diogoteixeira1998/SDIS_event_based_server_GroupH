import sqlite3
import sys
import time
from prettytable import PrettyTable



 

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
    print("Age:")  
    check_search=False     
    while(check_search==False):

        search_query = input()
        if(search_query.isdigit()):
            print("Searching......")
            check_search=True
        else:
            print("Please entre an integer")
        

    start = time.time()

    #   OPEN DATA BASE CONNECTION
    connection = connectDataBase('randomData.db')
    cursor = connection.cursor()

    end = time.time()
    time_connecting=(end - start)*1000
    start = time.time()


    #   SEARCH DATABASE FOR QUERY
    n_entries=0
    AVG_salary=0
    AVG_score= 0

    command = "SELECT * FROM personal_info WHERE Age=" + str(search_query)
    cursor.execute(command)
    output_raw = cursor.fetchall()
    if(output_raw):
        #print(output_raw, "\n\n")
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
        AVG_score = sum_salary/n_entries
        print(t) 
        print("Slaray avg:      ",  AVG_salary )
        print("Score avg:       ",  AVG_score  )
    else:
        print("No results\n")


    command2 = "INSERT INTO history ( Query, Total_entries, SalaryAVG, ScoreAVG, Time) VALUES ('"+ str(search_query) +"',"+ str(n_entries) +","+str(AVG_salary)+","+str(AVG_score)+",'"+ str(start) +"')"    
    cursor.execute(command2)
    connection.commit()

    
    cursor.execute("SELECT * FROM history")
    #print(cursor.fetchall())
    output_raw2 = cursor.fetchall()
    if(output_raw2):
        n_entries = len(output_raw2)
        t = PrettyTable(['code (PK)', 'Query', 'Total_entries', 'SalaryAVG', 'ScoreAVG', 'Time'])

        for column in output_raw2:
            t.add_row([column[0],  column[1],    column[2],    column[3],    column[4],    column[5]]) 
        
        print(t) 
    else:
        print("No results\n")
    
    
    end = time.time()
    time_search=(end - start)*1000
    start = time.time()

    #   CLOSE CONNECTION
    closeConnection(connection)

    end = time.time()
    time_closing=(end - start)*1000

    print( "Time connecting             ", time_connecting, "\n")
    print( "Time searching              ", time_search, "\n")
    print( "Time closing                ", time_closing, "\n")
    print( "TOTAL TIME ELAPSED:         ", time_connecting+time_search+time_closing, "\n")
    

################# Run code #######################    

main()
