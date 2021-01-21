import socket
import time
import ip_config

def client():
  HOST = ip_config.HOST  # The server's hostname or IP address

  PORT = ip_config.PORT   # The port used by the server

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((HOST, PORT))
      msg = input("-> ")


      HEADERSIZE        = 10
      new_data          = True
      data_received     = False
      full_data         = ""


      while msg != 'q':

        if msg != '' and msg.isdigit():  
          s.sendall(msg.encode())


          
          while not data_received:

            # receive package with size 16
            data = s.recv(16)

            # if firt package read header with the lenght of the full message
            if new_data:
              print("new msg len:",data[:HEADERSIZE])
              data_len = int(data[:HEADERSIZE])
              new_data = False

            full_data += data.decode()

            # full mesage received
            if len(full_data)-HEADERSIZE > data_len:
              print("full msg recvd")
              new_data = True
              data_received = True
              

          print('Received', full_data)
          full_data = ""
          data_received = False
        
        else:
          print("ERROR - Search request in not an integer")

        msg = input("-> ")

client()

