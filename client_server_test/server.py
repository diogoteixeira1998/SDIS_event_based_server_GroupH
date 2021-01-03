import socket

def server():
  HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
  PORT = 65433        # Port to listen on (non-privileged ports are > 1023)

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.bind((HOST, PORT))
      s.listen()
      conn, addr = s.accept()
      with conn:
          print('Connected by', addr)
          cont=0
          while True:
              data = conn.recv(1024)
              if not data:
                  break
              #conn.sendall(data)
              cont=cont+1
              conn.sendall(str(cont).encode())

#if __name__ = "__main__":
server()
