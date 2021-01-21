import threading
import time
import socket
import requests
import queue
import search_data_comm
import ip_config


# Global variables
value1 = []
value2 = []
value3 = []
value4 = []
value5 = []
connection = False
PACKAGE_SIZE = 16
HEADERSIZE   = 10

# QUEUES
request_list = []   # Requests that arrive from client
waiting_list_db1 = []
waiting_list_db2 = []
waiting_list_db3 = []
waiting_list_db4 = []
waiting_list_send = []


#===========================================
#  request_queue creates a new request and adds it to the request queue
#===========================================
def request_queue(data, connect, request_id):
    global request_list

    request = requests.Request(request_id, 0, connect, data, [], [], time.time(), 0, 0, 0, 0)
    request_list.append(request)


#===========================================
#  func1 - Search DB1, update request object and its state
#===========================================
def func1(event1, val1):
    global waiting_list_db2
    flag1 = event1.wait(timeout=0)
   
    if flag1:

        val1.result_db1 = search_data_comm.search_db(val1.search_val, 'randomData.db')

        val1.request_state = 1
        val1.t_thread1 = time.time()

        waiting_list_db2.append(val1)
        event1.clear()


    else:

        event1.clear()


#===========================================
#  func2 - Search DB2, update request object and its state
#===========================================
def func2(event2, val2):
    global waiting_list_db3
    flag2 = event2.wait(timeout=0)
  
    if flag2:

        val2.result_db2 = search_data_comm.search_db(val2.search_val, 'randomData2.db')

        val2.request_state = 2
        val2.t_thread2 = time.time()

        waiting_list_db3.append(val2)
        event2.clear()

    else:

        event2.clear()


#===========================================
#  func3 - Insert results in DB3, update request state
#===========================================
def func3(event3, val3):
    global waiting_list_db4
    flag3 = event3.wait(timeout=0)
  
    if flag3:

        search_data_comm.history_db(val3.result_db1, 'searchHistory2.db')
        val3.request_state = 3
        val3.t_thread3 = time.time()

        
        waiting_list_db4.append(val3)
        event3.clear()

    else:
        event3.clear()


#===========================================
#  func4 - Insert results in DB4, update request state
#===========================================
def func4(event4, val4):
    global waiting_list_send
    flag4 = event4.wait(timeout=0)
  
    if flag4:

        search_data_comm.history_db(val4.result_db2, 'searchHistory4.db')
        val4.request_state = 4
        val4.t_thread3 = time.time()

        
        waiting_list_send.append(val4)
        event4.clear()

    else:
        event4.clear()


#===========================================
#  server
#===========================================
def server():
    request_id = 0

    global connection

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip_config.HOST, ip_config.PORT))
        s.listen()
        conn, addr = s.accept()
        connection = conn
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(16)
                if not data:
                    break
                if data.isdigit():

                    request_queue(int(data.decode()), conn, request_id)
                    request_id = request_id + 1

                else:
                    print("not int")



#===========================================
#  send result to client
#===========================================
def send_client(event5, val5):

    global HEADERSIZE
    global PACKAGE_SIZE

    flag5 = event5.wait(timeout=0)

    if flag5:
        val5.request_state = 5
        val5.t_finish = time.time()

        aux_msg =  str(val5.result_db1) + str(val5.result_db2)
        full_msg = f"{len(aux_msg):<{HEADERSIZE}}" + aux_msg

        msg_sent = False
        i=0
        f=PACKAGE_SIZE
        print("\n\n",full_msg)

        # Send message in size 16 packages
        while not msg_sent:
            
            if(f>len(full_msg)):
                package = full_msg[i:f].ljust(PACKAGE_SIZE)
            else:
                package = full_msg[i:f]
            
            val5.connection.send(package.encode())
            i=i+PACKAGE_SIZE
            f=f+PACKAGE_SIZE
            if(i>len(full_msg)):
                msg_sent = True
        
        event5.clear()
    else:
        event5.clear()


def main():

    global value1
    global value2
    global value3
    global value4
    global value5

    event1 = threading.Event()
    event2 = threading.Event()
    event3 = threading.Event()
    event4 = threading.Event()
    event5 = threading.Event()

    global request_list
    global waiting_list_db1
    global waiting_list_db2
    global waiting_list_db3
    global waiting_list_send

    global connection


    # Begin Server Thread
    thread0 = threading.Thread(target=server)
    thread0.start()

    # Begin DataBase Threads
    thread1 = threading.Thread(target=func1, args=(event1, value1))
    thread2 = threading.Thread(target=func2, args=(event2, value2))
    thread3 = threading.Thread(target=func3, args=(event3, value3))
    thread4 = threading.Thread(target=func4, args=(event4, value4))
    thread5 = threading.Thread(target=send_client, args=(event5, value5))

    while True:

        time.sleep(0.001)

        # scheduler - if thread is free and there is a request for that thread -> call thread


        if not thread1.is_alive() and request_list:
            if request_list:
                request_to_send_db1 = request_list[0]
                request_list.pop(0)
                thread1 = threading.Thread(target=func1, args=(event1, request_to_send_db1))
                event1.set()
                thread1.start()
            else:
                continue

        if not thread2.is_alive() and waiting_list_db2:
            if waiting_list_db2:
                request_to_send_db2 = waiting_list_db2[0]
                waiting_list_db2.pop(0)
                thread2 = threading.Thread(target=func2, args=(event2, request_to_send_db2))
                event2.set()
                thread2.start()
            else:
                continue

        if not thread3.is_alive() and waiting_list_db3:
            if waiting_list_db3:
                request_to_send_db3 = waiting_list_db3[0]
                waiting_list_db3.pop(0)
                thread3 = threading.Thread(target=func3, args=(event3, request_to_send_db3))
                event3.set()
                thread3.start()
            else:
                continue

        if not thread4.is_alive() and waiting_list_db4:
            if waiting_list_db4:
                request_to_send_db4 = waiting_list_db4[0]
                waiting_list_db4.pop(0)
                thread4 = threading.Thread(target=func4, args=(event4, request_to_send_db4))
                event4.set()
                thread4.start()
            else:
                continue

        if not thread5.is_alive() and waiting_list_send:
            if waiting_list_send:
                request_to_send_send = waiting_list_send[0]
                waiting_list_send.pop(0)
                thread5 = threading.Thread(target=send_client, args=(event5, request_to_send_send))
                event5.set()
                thread5.start()
            else:
                continue



if __name__ == '__main__':
    main()
