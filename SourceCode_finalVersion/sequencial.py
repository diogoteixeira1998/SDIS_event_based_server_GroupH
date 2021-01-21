import threading
import time
import socket
import requests
import queue
import search_data_comm
import ip_config

# Global variables
value = []
connection = False
PACKAGE_SIZE = 16
HEADERSIZE   = 10


request_list = []   # Requests that arrive from client


#===========================================
#  request_queue creates a new request and adds it to the request queue
#===========================================
def request_queue(data, connect, request_id):
    global request_list

    request = requests.Request(request_id, 0, connect, data, [], [], time.time(), 0, 0, 0, 0)
    request_list.append(request)



#===========================================
#  func processes the request (Access data bases, calculation and sends the resut to clien)
#===========================================
def func(event, val):

    global PACKAGE_SIZE
    global HEADERSIZE

    flag = event.wait(timeout=0)

    if flag:

        # DB 1
        val.result_db1 = search_data_comm.search_db(val.search_val, 'randomData.db')
        val.request_state = 1
        val.t_thread1 = time.time()

        # DB 2
        val.result_db2 = search_data_comm.search_db(val.search_val, 'randomData2.db')
        val.request_state = 2
        val.t_thread2 = time.time()

        # DB 3
        search_data_comm.history_db(val.result_db1, 'searchHistory2.db')
        val.request_state = 3
        val.t_thread3 = time.time()

        # DB 4
        search_data_comm.history_db(val.result_db2, 'searchHistory4.db')
        val.request_state = 4
        val.t_thread3 = time.time()
        
        
        # SEND
        val.request_state = 5
        val.t_finish = time.time()

        aux_msg =  str(val.result_db1) + str(val.result_db2)
        full_msg = f"{len(aux_msg):<{HEADERSIZE}}" + aux_msg
        print(full_msg)

        msg_sent = False
        i=0
        f=16
        print(full_msg)
        while not msg_sent:
            
            if(f>len(full_msg)):
                package = full_msg[i:f].ljust(PACKAGE_SIZE)
            else:
                package = full_msg[i:f]
            
            val.connection.send(package.encode())
            i=i+PACKAGE_SIZE
            f=f+PACKAGE_SIZE
            if(i>len(full_msg)):
                msg_sent = True
        
        
        event.clear()


    else:

        event.clear()


#===========================================
#  server
#===========================================
def server():
    request_id = 0

    global request_list
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


def main():

    global value

    event = threading.Event()

    global request_list
    global connection


    # Begin Server Thread
    thread0 = threading.Thread(target=server)
    thread0.start()

    # Begin DataBase Threads
    thread = threading.Thread(target=func, args=(event, value))

    while True:

        time.sleep(0.001)


        # scheduler - if thread is free and there is request -> call thread
        if not thread.is_alive() and request_list:
            if request_list:
                request_to_send = request_list[0]
                request_list.pop(0)
                thread = threading.Thread(target=func, args=(event, request_to_send))
                event.set()
                thread.start()
            else:
                continue


if __name__ == '__main__':
    main()
