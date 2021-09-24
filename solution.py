# import socket module
from socket import *
# In order to terminate the program
import sys, os

def webServer(port=13331):
  serverSocket = socket(AF_INET, SOCK_STREAM)
  #Prepare a server socket
  serverSocket.bind(("", port))
  serverSocket.listen(1)
  while True:
    #Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
        try:
            message = connectionSocket.recv(2048)
            print("Received message: {}".format(message))
            filename = message.split()[1]
            f = open(filename[1:])
            outputdata = f.read()
            f.close()
            print("Ready to send output data: {}".format(outputdata))
            #Send one HTTP header line into socket.
            connectionSocket.send("HTTP/1.0 200 OK\r\n".encode())
            connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())
            #Send the content of the requested file to the client
            connectionSocket.send(outputdata.encode())
            connectionSocket.close()
        except IOError:
            connectionSocket.send("HTTP/1.0 404 Not Found\r\n".encode())
            connectionSocket.close()
    except (ConnectionResetError, BrokenPipeError) as e:
      pass
  serverSocket.close()
  sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
  webServer(13331)