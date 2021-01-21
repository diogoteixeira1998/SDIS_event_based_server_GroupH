import socket
import time
import threading
import ip_config
import random
import numpy as np

# Global var
connection      = []
limit           = 1
start_time      = 0
end_time        = 0
ready           = False

# TEST PARAMETERS
PERIOD          = 0.01
RANDOM_PERIOD   = False
MAX_SAMPLES     = 50

def client_send():


    global connection
    global PERIOD
    global limit
    global start_time
    global ready
    global RANDOM_PERIOD
    global MAX_SAMPLES
    cnt_send     = 0 
    PACKAGE_SIZE = 16


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip_config.HOST, ip_config.PORT))
        connection.append(s)

        msg=''

        while 1:

            # get a random serch request
            msg = str(random.randint(15, 35))
            
            # adjust message to fit in one package
            msg_right_size = "0"*(PACKAGE_SIZE-len(msg)) + msg
            print(cnt_send+1," search query: ", msg )

            if(RANDOM_PERIOD):
                # RANDOM PERIOD
                t_random = np.random.uniform(0.0, 0.05, 1) 
                time.sleep(t_random)
            else:
                time.sleep(PERIOD)
    
            

            # send request to server
            s.sendall(msg_right_size.encode())

            if cnt_send==0:
                start_time = time.time()
            cnt_send+=1

            if cnt_send>=limit:
                while not ready:
                    time.sleep(2)
                    print("\n\n\n")
                    if limit>MAX_SAMPLES:
                        print("TEST OVER")
                        time.sleep(600)
                ready = False
                cnt_send=0
                

def client_receive():

    global connection
    j=0
    global limit
    global start_time
    global end_time
    global ready

    HEADERSIZE        = 10
    PACKAGE_SIZE      = 16
    new_data          = True
    data_received     = False
    full_data         = ""

    while True:

        # test round over save results
        if j>=limit:
            end_time=time.time()
            delta = end_time - start_time
            f = open("results.csv", "a")
            f.write(str(limit)+","+str(delta)+"\n")
            f.close()
            start_time = 0
            end_time = 0
            delta = 0
            j = 0

            if limit<3000:
                limit = limit*2
            else:
                limit = limit*1.5

            ready = True

        
        while not data_received:

            # receive package with size 16
            data = connection[0].recv(PACKAGE_SIZE)

            # if firt package read header with the lenght of the full message
            if new_data:
                data_len = int(data[:HEADERSIZE].decode())
                new_data = False

            full_data += data.decode()

            # full mesage received
            if len(full_data)-HEADERSIZE > data_len:
                new_data = True
                data_received = True
              

        print("         Received:", full_data)
        full_data = ""
        data_received = False

        j+=1


def main():

    # run send and reaceive in two threads
    thread1 = threading.Thread(target=client_send)
    thread2 = threading.Thread(target=client_receive)
    thread1.start()
    time.sleep(1)
    thread2.start()



if __name__ == '__main__':
    main()



