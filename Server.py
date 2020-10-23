import socket
import select
import time

HEADER = 20

# Default for testing
HOST = 'localhost'
PORT = 65418  # Our default port

PORT = int(input("Escribe el puerto deseado: "))

clientes = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen()

lista_sockets = [s]


def recibir_msg(sck_cliente):
    try:
        cabecera = sck_cliente.recv(HEADER)
        lon = int(cabecera.decode().strip())
        return {'cabecera': cabecera, 'msg': sck_cliente.recv(lon)}
    except:  # Desconexión
        return False


print("Esperando conexiones...")
count = 0
while True:
    socket_lectura, vacio, excepciones = select.select(lista_sockets, [], lista_sockets)
    count += 1
    print(count)
    for sock in socket_lectura:
        # New connection
        if sock == s:
            conn, addr = s.accept()
            clientes.append(conn)
            lista_sockets.append(conn)
            print("Conexión desde", addr)
        # Message from socket
        else:
            msg = recibir_msg(sock)
            if msg is False:
                print("Usuario", sock, "desconectado")
                lista_sockets.remove(sock)
                clientes.remove(sock)
                continue
            dat = str(sock.getpeername()) + "|" + msg['msg'].decode()
            print(dat)

            # Text log
            named_tuple = time.localtime()  # get struct_time
            time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
            file = open('text_log.txt', 'a')
            file.write(time_string + "|" + dat + "\n")
            file.close()

            # Send message to other sockets
            for socket_cliente in clientes:
                if socket_cliente != sock:
                    socket_cliente.send(msg['cabecera'] + msg['msg'])

conn.close()
s.close()
