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
    dataIn = socket.recv(4096) #After the command is sent to command, it waits for the server's response and reads upto 4096 bytes
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

    command = "PASV" + "\r\n" # command is 'PASV' followed by terminator
    data = sendCommand(clientSocket, command) # sends PASV mode command to server
    print(data)

    status = 0
    if data.startswith("227"): # 227 indicates successful PASV initiation
        status = 227

        # create substring with information only
        start_index = data.find("(")
        terminal_index = data.find(")")
        information = data[start_index+1:terminal_index].split(",")

        ip = f"{information[0]}.{information[1]}.{information[2]}.{information[3]}" # convert ip
        port = int(information[4]) * 256 + int(information[5]) # calculate port

        print(f"Connecting to {ip} on port {port} for dataSocket!")

        # create new socket for data
        dataSocket = socket(AF_INET, SOCK_STREAM)
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
        dataIn = sendCommand(clientSocket, "USER " + username + "\r\n") # corrected mistake, should be 'USER' not 'USERNAME'
        print(dataIn)

      
        if dataIn.startswith("331"): #If the server responses with 331, it means the server is asking for password and I send the password.
            status = 331
            # COMPLETE
            print("Sending password")
            dataIn = sendCommand(clientSocket, "PASS " + password + "\r\n") # corrected mistake, should be 'PASS' not 'PASSWORD'
            
            print(dataIn)
            if dataIn.startswith("230"): # If the server responses with 230, it means the login is successful.
                status = 230
                print("Login has been Successful.")
    
    #************ Raiyan's Work Ends  for phase 1************************* #

    if dataIn.startswith("230"):
        status = 230
       
    if status == 230:
        # It is your choice whether to use ACTIVE or PASV mode. In any event:
        # COMPLETE
        while True:
            cmdline = input("myftp> ").strip()
            if not cmdline:
                continue
            parts = cmdline.split()
            cmd = parts[0].lower()
            
            # ************Raiyan's work start on Phase 2******** #
            if cmd == "quit":
                pass # remove when function is implemented!
                #implementation required 
                quitFTP(clientSocket)
                print("Disconnected from the server......")
                clientSocket.close()
                sys.exit(0)
            # ************Raiyan's work end on Phase 2******** #

            elif cmd == "cd":
                pass # remove when function is implemented!
                # implementation required
            
            elif cmd == "ls":
                # implementation required
                pasvStatus, dataSocket = modePASV(clientSocket)
                if pasvStatus == 227:
                    pass
                    # COMPLETE
            
            elif cmd == "get":
                pasvStatus, dataSocket = modePASV(clientSocket) # establish PASV

                # extract full file name
                filename = " ".join(parts[1:])
                if filename.startswith('"') and filename.endswith('"'):
                    filename = filename[1:-1]

                if pasvStatus == 227: # checks is pasv is established
                    processData = sendCommand(clientSocket, f"RETR {filename}\r\n")
                    print(processData)

                    if processData.startswith("150"): # data connection opened
                        data = bytearray()

                        # continue to read data until data is exhausted
                        while chunk := dataSocket.recv(4096):
                            data.extend(chunk)

                        # save data to file
                        with open(filename, "wb") as file:
                            file.write(data)

                    dataSocket.close()

                    # if data was 550, 226 cannot be returned. therefore check is required to prevent program from hang
                    if not processData.startswith("550"):
                        print(receiveData(clientSocket))

            elif cmd == "put":
                pasvStatus, dataSocket = modePASV(clientSocket) # establish PASV

                # extract full file name
                filename = " ".join(parts[1:])
                if filename.startswith('"') and filename.endswith('"'):
                    filename = filename[1:-1]

                if pasvStatus == 227: # checks if pasv is established
                    processData = sendCommand(clientSocket, f"STOR {filename}\r\n")
                    print(processData)

                    if processData.startswith("150"):
                        try:
                            dataSocket.sendfile(open(f"{filename}", "rb"))
                        except FileNotFoundError:
                            print("File not found! No data sent!")

                        dataSocket.close()

                    print(receiveData(clientSocket))

            elif cmd == "delete":
                pass # remove when function is implemented!
                # implementation required
            else:
                print("Invalid command. Supported commands are: ls, cd, get, put, quit.")
                continue
    
    

main()

