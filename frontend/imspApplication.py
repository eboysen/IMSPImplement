import socket

###################################################################################
#Gets the desired connection from the user and pings the                          #
#Server with a CHECK message to confirm that it is running IMSP                   #
#Input: connection- a string that contains the server being connected to          #
#Output: on Success returns serverHostName, otherwise empty string                #
###################################################################################
def checkConnection():
    serverHostName = input('What host would you like to connect to: ')
    print()
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((serverHostName,10000))
        s.send(str.encode('CHECK\n'+serverHostName))
        resp = s.recv(2000)
        resp = resp.decode()
        if(resp == '200'):
            print('Server OK')
            return serverHostName
        else:
            print('Sorry, that server does not appear to be running an IMSP Protocol on the default port')
            return ""
        s.close()
    except:
        print("Sorry, that server does not appear to be running an IMSP Protocol")
        return ""

###################################################################################
#Runs in main loop and allows user to decide which operation they                 #
#Would like to perform on the inventory management system                         #
#Input: connection- a string that contains the server being connected to          #
#Output: msg - a string that will be sent over the socket in correct IMSP format  #
###################################################################################
def makeChoice(conn):
    msg = ""
    #determine user operation for connection
    print()
    print('What operation would you like to perform')
    print('(1): Print Inventory')
    print('(2): Update an item inventory')
    print('(3): Delete an item from the inventory')
    print('(4): Exit application')
    operation = input('Choice: ')
    print(operation)
    #handle operation accordingly to construct message
    
    if operation =="1":
        print()
        msg=getMsg(conn)
    elif operation =="2":
        print()
        msg=updateMsg(conn)
    elif operation =="3":
        print()
        msg=deleteMsg(conn)
    elif operation =="4":
        msg = "exit"
    else:
        print('That is not an allowed option, please choose one of the allowed options.')
        return makeChoice(conn)
    return msg

###################################################################################
#Runs when the user decides to operate on the inventory                           #
#System by getting full readout of the inventory sorted as specified              #
#Input: connection- a string that contains the server being connected to          #
#Output: msg - a string that will be sent over the socket in correct IMSP format  #
###################################################################################
def getMsg(connection):
    msg="GET "+connection+"\n"
    print("(1): Sort by Name")
    print("(2): Sort by Quantity")
    print("(3): Sort by Inventory Date")
    print("(4): Cancel")
    choice = input('Which way would you like to sort the inventory:')
    if(choice == '4'):
        print()
        return makeChoice(connection)
    else:
        msg+=choice
    return msg

###################################################################################
#Runs when the user decides to operate on the inventory                           #
#System by updating an item's inventory quantity                                  #
#Input: connection- a string that contains the server being connected to          #
#Output: msg - a string that will be sent over the socket in correct IMSP format  #
###################################################################################
def updateMsg(connection):
    msg = "UPDATE "+connection+"\n"
    msg+= input('Please specify the name of the item that you would like to delete from the inventory system: ')
    msg+= " "+input('Please specify the new quantity: ')
    return msg

###################################################################################
#Runs when user decides to opperate on the inventory                              #
#System by deleting an item                                                       #
#Input: connection- a string that contains the server being connected to          #
#Output: msg - a string that will be sent over the socket in correct IMSP format  #
###################################################################################
def deleteMsg(connection):
    msg = "DELETE "+connection+"\n"
    msg+= input('Please specify the name of the item that you would like to delete from the inventory system: ')
    return msg





######################################################################
#Start procedural code
######################################################################

#tracks program loop
mainLoop = True
#holds the ip of the server connection
connection = ""

print('---------Welcome to IMSP---------')
print()
print()


while connection=="":
    #Keep trying to connect to a valid IMSP Server
    connection = checkConnection()

#main program loop
while mainLoop:
    #connect to socket
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    #Run functions to choose an opperation and build a correct IMSP protocol message
    message = makeChoice(connection)
    #print(message)
    
    #send constructed message or exit the program
    if message == "exit":
        mainLoop = False
    else:
        #open a connection to the IMSP server on the default IMSP port
        s.connect((connection,10000))
        s.send(str.encode(message))

        #Process the response from the server
        resp = s.recv(2000)
        resp = resp.decode()
        print("Echo: "+resp)

        #close the connection since IMSP is a stateless/ non-persistant protocol
        s.close()
print('ThAnk YoU fOr FlyinG AmerIcan')

