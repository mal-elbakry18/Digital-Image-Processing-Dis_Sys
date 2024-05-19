import zmq 
from time import sleep
#import socket

#set up 
context = zmq.Context()

#set up soket that is where the clients/subscribers will listen from 
socket = context.socket(zmq.PUB)

#bind the socket
socket.bind('tcp://127.0.0.1:2000')

#setting up the logic 

#create list of meassage
messages= [100,200,300]

curr_msg = 0 #index of the message

while(True):
    print("Publisher is listening")
    sleep(1) #sleep for one sec
    socket.send_pyobj({curr_msg:messages[curr_msg]})
    if(curr_msg ==2):
        curr_msg = 0
    else:
        curr_msg=curr_msg+1

