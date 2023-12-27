# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 12:47:00 2021

@author: ehalep
"""
#Import the socket library
from struct import *
import socket
import binascii
from _thread import *

#Η συνάρτηση που θα διαχειρίζεται τα connection
#Είναι όπως κάθε άλλη συνάρτηση, απλά θα τρέχει αυτόνομα από το άλλο πρόγραμμα.
def threaded_client(conn, addr):
    #Print info: Connected address, Server IP & Port, Client IP & Port
    print("Thread to handle connection by:", addr)
    print("Server Socket port: ", conn.getsockname())
    print("Client Socket port: ", conn.getpeername())

    while(1):
        
        msg = conn.recv(12)

        
        msg_type,msg_length,msg_Symbol,msg_num1,msg_num2,msg_id = unpack('HHHHHH', msg)
        
        print('Total message length ='+str(msg_length))
        
      
        
        
        
        
        

        
        msg_type = 1
        
        msg_response_code = 0
        if (msg_Symbol == 4) or (msg_Symbol == 3) or (msg_Symbol== 1)  :
            if ((msg_num1 < 0) or (msg_num1 >60000)) or ((msg_num2<0) or (msg_num2>60000)):
                msg_response_code = 1
        if (msg_Symbol==3) and (msg_num2==0):
            msg_response_code=2
        if (msg_Symbol==2) and (msg_num1>30000 or msg_num1<0 or msg_num2>30000 or msg_num2<0):
            msg_response_code=3



        if(msg_Symbol==4):
            msg_response=msg_num1+msg_num2
        elif(msg_Symbol==2):
            msg_response=msg_num1-msg_num2
        elif(msg_Symbol==3):
            msg_response=msg_num1/msg_num2
        elif(msg_Symbol==1):
            msg_response=msg_num1*msg_num2
        else:
            msg_response=0
            msg_response_code=4       


        if msg_response>0:
            msg_proth=1
        else:
            msg_proth=2    

        print(msg_proth,msg_response)
        #Now it's time to pack our response.
        message = pack('HHHHI', msg_type,msg_proth,msg_id, msg_response_code,msg_response)
        #Send the message through the same connection
        err = conn.sendall(message)
        #Print any errors if any exist
        print(err)

#Host IP to listen to. If '' then all IPs in this interface
serverIP = ''
#Port to listen to
serverPort = 12345
#Flag to close the socket. Normally we don't close the socket. We keep on listening. 
#This flag is used to simply terminate the program and close the socket as we don't need it after
#the message exchange
close = False

#Create the server socker
#socket.AF_INET == IPv4
#socket.SOCK_STREAM == TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
    #Bind the socket
    serverSocket.bind((serverIP, serverPort))
    print ("The server is ready to receive at port", str(serverPort))
    #Listen for connections
    #If we don't specify in the listen a number e.g. serverSocket.listen(5), it goes to the system default
    serverSocket.listen()
    ThreadCount=0
    while not close:
        conn, addr = serverSocket.accept()
        #Listen and wait for connection
        #Once a connection is made it returns two values, the conn will have the connection socket and the addr will have the address
        #These will be passed to the Thread to handle the connection. The main program will go on
        start_new_thread(threaded_client, (conn, addr))
        ThreadCount+=1
        print('Thread Number: ' + str(ThreadCount))

        #Signal (with the flag) to close the socket
        #close=True
        #Close when Thread reaches 5
        if ThreadCount==5:
            serverSocket.close()