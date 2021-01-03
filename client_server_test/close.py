import socket

def close():
  host = socket.gethostname()   # get local machine name
  print(host)
  host = '127.0.0.1'
  print(host)
  port = 65432 # Make sure it's within the > 1024 $$ <65535 range
  
  s = socket.socket()
  s.bind((host, port))

  s.close()



close()
