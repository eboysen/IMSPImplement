import socket

thing = True
print('---------Welcome to IMSP---------')
print()
print()
while thing:
    #print('please try again')
    #print('starting socket')
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('connecting socket')
    s.connect(('localhost',3000))
    UI = input('input:')
    if UI == "exit":
        thing = False
        s.close()
    else:
        
        s.send(str.encode(UI))
        #print('sent message')
        resp = s.recv(2000)
        resp = resp.decode()
        print("Echo: "+resp)
        s.close()
print('ThAnk YoU fOr FlyinG AmerIcan')

