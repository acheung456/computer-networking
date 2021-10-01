from socket import *


def smtp_client(port=1025, mailserver='127.0.0.1'):
   msg = "\r\n My message"
   endmsg = "\r\n.\r\n"

   # Choose a mail server (e.g. Google mail server) if you want to verify the script beyond GradeScope

   # Create socket called clientSocket and establish a TCP connection with mailserver and port

   clientSocket = socket(AF_INET, SOCK_STREAM)
   clientSocket.connect(mailserver, port)


   recv = clientSocket.recv(1024).decode()
   print(recv)
   if recv[:3] != '220':
       pass
       #print('220 reply not received from server.')

   # Send HELO command and print server response.
   heloCommand = 'HELO Alice\r\n'
   clientSocket.send(heloCommand.encode())
   recv1 = clientSocket.recv(1024).decode()
   print(recv1)
   if recv1[:3] != '250':
       pass
       #print('250 reply not received from server.')

   # Send MAIL FROM command and print server response.
   clientSocket.send("MAIL FROM:johnnyappleseed\r\n".encode())
   recv2 = clientSocket.recv(1024).decode()
   #print(recv2)

   # Send RCPT TO command and print server response.
   clientSocket.send("RCPT TO:johnnyappleseed\r\n".encode())
   recv3 = clientSocket.recv(1024).decode()
   #print(recv3)

   # Send DATA command and print server response.
   clientSocket.send("DATA\r\n".encode())
   recv4 = clientSocket.recv(1024).decode()
   #print(recv4)

   # Send message data.
   clientSocket.send("Subject: Would be weird without one\r\n\r\n".encode())
   clientSocket.send("Wed, 12 April 1989 11:00:00\r\n\r\n".encode())
   clientSocket.send("\r\nThe Message".encode())


   # Message ends with a single period.
   clientSocket.send("\r\n.\r\n".encode())
   recv5 = clientSocket.recv(1024).decode()

   # Send QUIT command and get server response.
   clientSocket.send("QUIT\r\n".encode())
   recv6 = clientSocket.recv(1024).decode()
   clientSocket.close()


if __name__ == '__main__':
   smtp_client(1025, '127.0.0.1')
