from http import client
from struct import *
import socket 
import binascii
import random
import time

serverIP='127.0.0.1'
serverPort = 12345
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverIP, serverPort))
msg_num1 = int(input("Enter the first Number : "))
msg_num2 = int(input("Enter the second Number : "))
symbol = input ("Enter the type of the calculation you want to do : ")
msg_length = 12
msg_type = 0 
msg_id=random.randrange(1, 65000)
if(symbol=="*"):
    msg_symbol=1
elif(symbol=="-"):
    msg_symbol=2
elif(symbol=="/"):
    msg_symbol=3
elif(symbol=="+"):
    msg_symbol=4
else:
    msg_symbol=0

print(msg_num1,msg_num2)
packString = 'HHHHHH'
message = pack(packString,msg_type,msg_length,msg_symbol,msg_num1,msg_num2,msg_id)
clientSocket.sendall(message)






modifiedMessage = clientSocket.recv(12)
#Unpack the message
msg_typeS,msg_prothS,msg_idS, msg_response_codeS,msg_responseS  = unpack('HHHHI', modifiedMessage)
#Print it as hex just for the fun of it
print(binascii.hexlify(modifiedMessage))
if(msg_id == msg_idS):
    print("This is my response")
    print("Type is "+str(msg_type)+ " and response code is "+str(msg_response_codeS))
    if(msg_response_codeS==0):
        if(msg_prothS==1):
            print("All went well")
            print("the outcome is +",msg_responseS)
        else:
            print("All went well")
            print("the outcome is -",msg_responseS)   
    elif(msg_response_codeS==1):
        print("Number out of bounds")
    elif(msg_response_codeS==2):
        print("Cant devide by 0...")
    elif(msg_response_codeS==3):
        print("Number out of bounds")
    elif(msg_response_codeS==4):
      print("Not a Valid Request")      
else:
    print("This is not my response")

time.sleep(5)    

#Close the socket
clientSocket.close()