# Help: https://www.eventhelix.com/networking/ftp/
# Help: https://www.eventhelix.com/networking/ftp/FTP_Port_21.pdf
# Help: https://realpython.com/python-sockets/
# Help: PASV mode may be easier in the long run. Active mode works 
# Reading: https://unix.stackexchange.com/questions/93566/ls-command-in-ftp-not-working
# Reading: https://stackoverflow.com/questions/14498331/what-should-be-the-ftp-response-to-pasv-command

#import socket module
from socket import *
import sys # In order to terminate the program


# This function was already "Almost" completed by skeleton. The first line was added by Raiyan
def quitFTP(clientSocket):
    # COMPLETE
    command = "QUIT\r\n" #Only this line is added to this function. #\r\n is FTP protocol requirement for the end of command. 
    dataOut = command.encode("utf-8")
    clientSocket.sendall(dataOut)
    dataIn = clientSocket.recv(1024)
    data = dataIn.decode("utf-8")
    print(data)

# The function below is completed by Raiyan
def sendCommand(socket, command):

    dataOut = command.encode("utf-8")  #This basically converts the text command into bytes

    # Complete

    socket.sendall(dataOut) #the sendall method basically sends the endtire command to the FTP server
    dataIn= socket.recv(4096) #After the command is sent to command, it waits for the server's response and reads upto 4096 bytes
    data = dataIn.decode("utf-8") # The server's response comes in bytes and 
    # it basically converts the bytes received from server to string. 

    return data 



def receiveData(clientSocket):
    dataIn = clientSocket.recv(1024)
    data = dataIn.decode("utf-8")
    return data

# If you use passive mode you may want to use this method but you have to complete it
# You will not be penalized if you don't
def modePASV(clientSocket):
    command = "PASV" + "\r\n"
    # Complete
    status = 0
    if data.startswith(""):
        status = 227
        # Complete
        dataSocket.connect((ip, port))
        
    return status, dataSocket

    
    
def main():
    #************ Raiyan's Work Starts for phase 1 ************************* #

    # COMPLETE

    if len(sys.argv) != 2:
        print("There should be only 1 argument which is the server-name. Write it like: python myftp.py server-name ")
        sys.exit(1)

    username = input("Enter the username: ")
    password = input("Enter the password: ")

    clientSocket = socket(AF_INET, SOCK_STREAM) # A new socket object is created here. Since we are using SOCK_STREAM, we are using TCP. 
    # COMPLETE

    HOST =  sys.argv[1] #Host is basically the Server. argv[1] is pulling the hostname from command line. 
    clientSocket.connect((HOST, 21)) # Here we are connecting to the server at port 21. 

    

    dataIn = receiveData(clientSocket) # After the connection request is sent to server, I am basically waiting for Server's response. 
    print(dataIn)

    status = 0
    
    if dataIn.startswith("220"): #If the server responses with 220, it means the server is ready to accept a login and I send the username. 
        status = 220
        print("Sending username")
        # COMPLETE
        dataIn = sendCommand(clientSocket, "USERNAME " + username + "\r\n")
        print(dataIn)

      
        if dataIn.startswith("331"): #If the server responses with 331, it means the server is asking for password and I send the password.
            status = 331
            # COMPLETE
            print("Sending password")
            dataIn = sendCommand(clientSocket, "PASSWORD " + password + "\r\n")
            
            print(dataIn)
            if dataIn.startswith("230"): # If the server responses with 230, it means the login is successful.
                status = 230
                print("Login has been Successful.")
    
    #************ Raiyan's Work Ends  for phase 1************************* #

       
    if status == 230:
        # It is your choice whether to use ACTIVE or PASV mode. In any event:
        # COMPLETE
        pasvStatus, dataSocket = modePASV(clientSocket)
        if pasvStatus == 227:
            # COMPLETE
    
    print("Disconnecting...")
    

    clientSocket.close()
    dataSocket.close()
    
    sys.exit()#Terminate the program after sending the corresponding data

main()

