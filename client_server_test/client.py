import socket

def client():
  HOST = '127.0.0.1'  # The server's hostname or IP address
  PORT = 65433        # The port used by the server

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((HOST, PORT))
      msg = input("-> ")

      while msg != 'q':
        #msg = input("-> ")
        #s.sendall(b'Hello, world')
        if msg != '':
          s.sendall(msg.encode())
          data = s.recv(1024)
          print('Received', repr(data.decode()))
        msg = input("-> ")

  #print('Received', repr(data))

#if __name__ = "__main__":
client()
