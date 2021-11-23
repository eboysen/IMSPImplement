import socketserver
import threading
PATH = './inventoryFile.txt'
def readFromFile():
    file = open(PATH,'r')
    lines = file.readlines()
    x = 0
    end = len(lines)
    while x < end:
        lines[x] = lines[x].split()
        #print(lines[x])
        x+=1
    file.close()
    return lines

def countingSort(arr, ind, code):
    print(arr)
    counting = [0]*128
    if(len(arr)==1):
        print('array length 1')
        return arr
    Duplicated = True
    dupNum = arr[0][code]
    if(ind == len(arr[0][code])):
        last = countingSort(arr[1:],ind,code)
        last.insert(0,arr[0])
        print('index full')
        return last
    
    maxLen = 0
    for item in arr:
        if len(item[code])>maxLen:
            maxLen = len(item[code])
    x = 0
    zeros = 0
    if(abs(ind)>maxLen):
        print("maxed")
        return arr
    while x<len(arr):
        print("index:{}".format(ind))
        print("code: {}".format(len(arr[x][code])))
        
        if(arr[x][code]!=dupNum):
            Duplicated=False
        if(ind == len(arr[x][code]) and code == 0):
            dup = arr[x]
            arr.pop(x)
            first = countingSort(arr,ind,code)
            first.insert(0,dup)
            print('first')
            print(first)
            return first
        elif(abs(ind) > len(arr[x][code]) and code !=0):
            zeros+=1
            arr[x][code]='0'+arr[x][code]
            print(ord(arr[x][code][ind]))
            counting[ord(arr[x][code][ind])]+=1 
        else:
            print(ord(arr[x][code][ind]))
            counting[ord(arr[x][code][ind])]+=1
        x+=1
    print(zeros)
    print(len(arr))

    #for x in arr:
     #   print(ord(x[code][ind]))
      #  counting[ord(x[code][ind])]+=1
    y = 1
    while y< len(counting):
        counting[y]+=counting[y-1]
        y+=1
    #print(counting)
    fin = [""]*len(arr)
    x = 0
    while x <len(arr):

        fin[counting[ord(arr[x][code][ind])-1]]=arr[x]
        counting[ord(arr[x][code][ind])-1]+=1
        x+=1
    #print(counting)
    y = 1
    #print(counting)
    while y< len(counting):
        #print(counting[y]-counting[y-1])
        if counting[y]-counting[y-1]>0:
            if code ==0:
                repl = countingSort(fin[counting[y-1]:counting[y]],ind+1,code)
            else:
                repl = countingSort(fin,ind-1,code)
                print(repl)
                return repl
            a = counting[y-1]
            b = 0
            while a< counting[y]:
                fin[a] = repl[b]
                a+=1
                b+=1
        if y==len(counting)-1 and counting[y]<len(fin):
            if code==0:
                repl =countingSort(fin[counting[y]:len(fin)],ind+1,code)
            else:
                return countingSort(fin,ind-1,code)
            a = counting[y]
            b = 0
            while a<len(fin):
                fin[a]=repl[b]
                a+=1
                b+=1
        y+=1
    return fin

def msdRadixSort(code):
    arr = readFromFile()
    if(code ==0):
        fin = countingSort(arr,0,code)
    else:
        fin = countingSort(arr,-1,code)
    for item in fin:
        print('a')
        print(item)
    return fin

def binarySearch():
    print()

def handleGet():
    print()

def handleUpdate(item):
    print()
    msdRadixSort()
    binarySearch(item)

def handleDelete(item):
    print()
    msdRadixSort()
    binarySearch(item)

class IMSPRequestHandler(socketserver.BaseRequestHandler):
    def _init_(self,request,client_address,server):
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)
        return
    def setup(self):
        print('setup request')
        return socketserver.BaseRequestHandler.setup(self)

    def handle(self):
        print('handle request')

        # Echo the back to the client
        package = self.request.recv(2000)
        package = package.decode()
        line = package.split("\n")
        lineOne = line[0].split(' ')
        outgoing = "RESPONSE "+self.client_address[0]+"\n"
        if(lineOne[0] == 'CHECK'):
            outgoing += "200"
        elif(lineOne[0]=='GET'):
            print()
            msdRadixSort()
        elif(lineOne[0]=='UPDATE'):
            print()
        elif(lineOne[0]=='DELETE'):
            print()
        else:
            outgoing+=400
        self.request.send(str.encode(outgoing))
        return

    def finish(self):
        print('finished request')
        return socketserver.BaseRequestHandler.finish(self)

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

msdRadixSort(2-1)
address = ('localhost',10000)
server = IMSPServer(address,IMSPRequestHandler)
ip, port = server.server_address
print('ip'+ip)
print(port)
t = threading.Thread(target=server.serve_forever)
t.start()
