###########################################################################################################
#                                                                                                         #
# +++++++++++++++++++++++++++++++++++++++++ IMSP SERVER +++++++++++++++++++++++++++++++++++++++++++++++++ #
#                                                                                                         #
#                                                                                                         #
# Author: Eric Boysen                                                                                     #
# Last Updated: 11/23/2021                                                                                #
# Description: Program to run a server which manages an inventory system using IMSP Protocol              #
#                                                                                                         #
#                                                                                                         #
###########################################################################################################



###########################################################################################################
# -----------------------------------------------Imports--------------------------------------------------#
###########################################################################################################
import socketserver
import threading
from tabulate import tabulate
from datetime import datetime

###########################################################################################################
# -----------------------------------------------Constants------------------------------------------------#
###########################################################################################################
PATH = './inventoryFile.txt'
ADDRESS = ('localhost',10000)

###########################################################################################################

###########################################################################################################
# -----------------------------------------Start Functional Code------------------------------------------#
###########################################################################################################

###################################################################################
#--------------------------------Read from File---------------------------------- #
#                                                                                 #
# Author: Eric Boysen                                                             #
# Last Updated: 11/23/2021                                                        #
#                                                                                 #
# Reads the contents of the inventory file and creates an array of tuples         #
# Each containing the Name(0), Quantity(1), and Date(2) of an item                #
#                                                                                 #
# Input: None                                                                     #
# Output: Item array [n][3]                                                       #
###################################################################################
def readFromFile():
    file = open(PATH,'r')
    lines = file.readlines()#reads line into array
    x = 0
    end = len(lines)
    #loop through and turn each line into a 3-tuple
    while x < end:
        lines[x] = lines[x].split()
        x+=1
    file.close()
    return lines

###################################################################################
#--------------------------------Counting Sort----------------------------------- #
#                                                                                 #                    
# Author: Eric Boysen                                                             #
# Last Updated: 11/23/2021                                                        #
#                                                                                 # 
# Uses the counting sort algorithm recursively to enable a radix sort algorithm   #
#                                                                                 #
# Input: arr- array of item tupes, ind - index operating on, code - which value   #
#       is sorting                                                                #
# Output: an array sorted in ascending order based on the desired attribute       #
###################################################################################
def countingSort(arr, ind, code):
    counting = [0]*128 # initialize an array to count digits in

    if(len(arr)==1):#base case for msd radix. If recurssion yeilds length 1 return arr
        return arr
        
    
    if(ind == len(arr[0][code])):#if the first word has maxed out its index attempt on rest of array
        last = countingSort(arr[1:],ind,code)
        last.insert(0,arr[0])# append first word back to front of arr
        return last
    
    maxLen = 0 #Find the string of longest length
    for item in arr:
        if len(item[code])>maxLen:
            maxLen = len(item[code])

    x = 0
    zeros = 0

    if(abs(ind)>maxLen): #base case for lsd radix when we reach max length
        return arr

    #Loops through and increments the digits of counting or handles edge cases    
    while x<len(arr):
        if(ind == len(arr[x][code]) and code == 0): # check if index reaches end of string and using msd
            dup = arr[x]#copies and removes so that we can sort remainder of arr
            arr.pop(x)
            first = countingSort(arr,ind,code)
            first.insert(0,dup)#adds back to the front of the array after sorting completed
            return first
        elif(abs(ind) > len(arr[x][code]) and code !=0):
            zeros+=1 #show that one more index is completed 
            arr[x][code]='0'+arr[x][code] # add a zero to the front of the index for later use in sorting
            counting[ord(arr[x][code][ind])]+=1 #add to 0 digits in counting
        else:
            counting[ord(arr[x][code][ind])]+=1 # increment appropriate digit
        x+=1


    y = 1
    #Show accumulation to convert digit counts into indecies
    while y< len(counting):
        counting[y]+=counting[y-1]
        y+=1

    fin = [""]*len(arr) #final array for return


    x = 0
    #Loop through array and add them to the correct position of fin
    while x <len(arr):
        fin[counting[ord(arr[x][code][ind])-1]]=arr[x]#use the position one behind and increment going up instead of down to maintain order
        counting[ord(arr[x][code][ind])-1]+=1
        x+=1


    y = 1
    #Makes recurrsive calls
    while y< len(counting):
        if counting[y]-counting[y-1]>0:#Only run if the difference between #'s is greater than 0
            if code ==0:#increment up if using msd
                repl = countingSort(fin[counting[y-1]:counting[y]],ind+1,code)
            else:#increment down if using lsd
                repl = countingSort(fin,ind-1,code)
                return repl
            a = counting[y-1]
            b = 0
            while a< counting[y]:#tranfer over changes made by recursive calls
                fin[a] = repl[b]
                a+=1
                b+=1
        if y==len(counting)-1 and counting[y]<len(fin):#Also run if at the end of array
            if code==0:#increment up if msd
                repl =countingSort(fin[counting[y]:len(fin)],ind+1,code)
            else:#increment down if lsd
                return countingSort(fin,ind-1,code)
            a = counting[y]
            b = 0
            while a<len(fin):#transfer over changes made by recursive calls
                fin[a]=repl[b]
                a+=1
                b+=1
        y+=1

    return fin


###################################################################################
#--------------------------------Radix Sort-------------------------------------- #
#                                                                                 #
# Author: Eric Boysen                                                             #
# Last Updated: 11/23/2021                                                        #
#                                                                                 #
# Used to initialize the radix sort on the inventory as necessary                 #
#                                                                                 #
# Input: code - int 0-2 to determine which attribute to sort on Name(0),          #
#        Quantity(1), Date(1)                                                     #
# Output: returns a sorted array of values from the inventory file                #
###################################################################################
def msdRadixSort(code):
    arr = readFromFile()
    if(code ==0):
        fin = countingSort(arr,0,code)
    else:
        fin = countingSort(arr,-1,code)
    for item in fin:
        print(item)
    return fin

###################################################################################
#--------------------------------Handle Get-------------------------------------- #
#                                                                                 #
# Author: Eric Boysen                                                             #
# Last Updated: 11/23/2021                                                        #
#                                                                                 #
# Used to build the response message for a get request sorted as requested        #
#                                                                                 #
# Input: code - int 0-2 to determine which attribute to sort on Name(0),          #
#        Quantity(1), Date(1)                                                     #
# Output: returns a sorted array of values in body of a response message          #
###################################################################################
def handleGet(code):
    msg = ""
    print(code)
    if(int(code) > 3 or int(code) < 1):#If the user requests an invalid code send back 400 code
        print("went through")
        return "400"
    try:
        sortedInv = msdRadixSort(int(code)-1)
        sortedInv = tabulate(sortedInv,headers = ["Name","Quantity","Date"])#tabulate into readable format

        #write to a new file in the updated format
        f= open("temp.txt", "w+")
        f.write(sortedInv)
        f.close()

        #open new file and read its contents into a variable for easy addition
        file = open("temp.txt","r")
        contents = file.read()
        file.close()

        #append the OK status and contents to the message
        msg+="200\n\n"+contents
    except:
        #if an error occurs report server error in message 
        return "300"
    return msg
    

###################################################################################
#--------------------------------Handle Update----------------------------------- #
#                                                                                 #
# Author: Eric Boysen                                                             #
# Last Updated: 11/23/2021                                                        #
#                                                                                 #
# Used to build the response message for an update request and update file        #
#                                                                                 #
# Input: item - name of desired item update, quantity: new quantity of item       #
# Output: returns a message with response code and data for update                #
###################################################################################
def handleUpdate(item,quantity):
    print()
    try:
        contents = readFromFile()
        x = 0
        while x< len(contents):
            if contents[x][0]==item:
                contents.pop(x)
            x+=1
        file = open(PATH, 'w+')
        for it in contents:
            file.write(it[0]+ " "+ it[1]+" "+it[2]+"\n")
        file.write(item + " " + quantity + " " + datetime.today().strftime('%Y/%m/%d') +"\n")
        file.close()
        return "200\n\nItem successfully updated"
    except:
        return "300"


###################################################################################
#--------------------------------Handle Delete----------------------------------- #
#                                                                                 #
# Author: Eric Boysen                                                             #
# Last Updated: 11/23/2021                                                        #
#                                                                                 #
# Used to build the response message for an delete request and update file        #
#                                                                                 #
# Input: item - name of desired item update                                       #
# Output: returns a message with response code and data for delete                #
###################################################################################
def handleDelete(item):
    print()
    try:
        contents = readFromFile()
        x = 0
        while x< len(contents):
            if contents[x][0]==item:
                contents.pop(x)
            x+=1
        file = open(PATH, 'w+')
        for it in contents:
            file.write(it[0]+ " "+ it[1]+" "+it[2]+"\n")
        file.close()
        return "200\n\nItem successfully deleted"
    except:
        return "300"


###########################################################################################################
# --------------------------------------------Handler Class-----------------------------------------------#
###########################################################################################################
#This is a socket server request handler implementation. Only handle is changed from default implementation
class IMSPRequestHandler(socketserver.BaseRequestHandler):
    def _init_(self,request,client_address,server):
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)
        return
    def setup(self):
        print('setup request')
        return socketserver.BaseRequestHandler.setup(self)

    def handle(self):
        print('handle request')

        # Get a request from socket
        package = self.request.recv(2000)
        package = package.decode()

        #split lines
        line = package.split("\n")
        lineOne = line[0].split(' ')

        #construct first part of the response header
        outgoing = "RESPONSE "+self.client_address[0]+"\n"

        #check what type of request is made and call appropriate function
        if(lineOne[0] == 'CHECK'):
            outgoing += "200"
        elif(lineOne[0]=='GET'):
            print(line[1])
            outgoing+=handleGet(line[1])
        elif(lineOne[0]=='UPDATE'):
            print()
            lineTwo = line[1].split()
            outgoing+=handleUpdate(lineTwo[0],lineTwo[1])
        elif(lineOne[0]=='DELETE'):
            print()
            outgoing+=handleDelete(line[1])
        else:#If non known request send invalid request code
            outgoing+=400
        
        #send the response message
        self.request.send(str.encode(outgoing))
        return

    def finish(self):
        print('finished request')
        return socketserver.BaseRequestHandler.finish(self)


###########################################################################################################
# -----------------------------------------Server Socket Class--------------------------------------------#
###########################################################################################################
#This is a default implementation of the server socket TCP server but uses the handler class above
class IMSPServer(socketserver.TCPServer):
    def __init__(self, server_address, handler_class=IMSPRequestHandler):
        print('IMSP server initialized')
        socketserver.TCPServer.__init__(self, server_address, handler_class)
        return

    def server_activate(self):
        print('IMSP server running')
        socketserver.TCPServer.server_activate(self)
        return

    def serve_forever(self):
        print('IMSP server running')
        while True:
            self.handle_request()
        return

    def handle_request(self):
        print('handling request\n')
        return socketserver.TCPServer.handle_request(self)

    def verify_request(self, request, client_address):
        print('verifying request\n')
        return socketserver.TCPServer.verify_request(self, request, client_address)

    def process_request(self, request, client_address):
        print('processing request\n')
        return socketserver.TCPServer.process_request(self, request, client_address)

    def server_close(self):
        print('closing server\n')
        return socketserver.TCPServer.server_close(self)

    def finish_request(self, request, client_address):
        print('finished request')
        return socketserver.TCPServer.finish_request(self, request, client_address)

    def close_request(self, request_address):
        print('closed request')
        return socketserver.TCPServer.close_request(self, request_address)


###########################################################################################################
# -----------------------------------------Start Procedural Code------------------------------------------#
###########################################################################################################

#Initialize socketsever and output information
server = IMSPServer(ADDRESS,IMSPRequestHandler)
ip, port = server.server_address
print('Request from IP Address: '+ip)
print('On Port: '+str(port))

#Begin running server on thread loop
t = threading.Thread(target=server.serve_forever)
t.start()
