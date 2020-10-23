import socket
import sys
import msvcrt

HEADER = 20

# Default for testing
HOST = 'localhost'
PORT = 65418

HOST = input("Introduce la dirección IP: ")
PORT = int(input("Introduce el puerto asignado: "))
usuario = input("Nombre de usuario: ")
print(PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.setblocking(False)
string = []
line = ""
sys.stdout.write(usuario + ": ")
sys.stdout.flush()
while True:
    # Key pressed
    if msvcrt.kbhit():
        try:
            char = msvcrt.getch()
            # If char is enter, send message
            if char == b'\r':
                line = ''.join(string)
                string = []
                msg = usuario + ": " + line
                cabecera_msg = f"{len(msg):<{HEADER}}".encode()
                s.send(cabecera_msg + msg.encode())
                line = ""
                sys.stdout.write('\n')
                sys.stdout.write(usuario + ": ")
                sys.stdout.flush()
                continue
            # Backspace
            elif char == b'\x08':

                # If there's no string left stop deleting
                if not string:
                    continue
                # Delete last character from string and terminal
                string.pop()
                char = char.decode()
                sys.stdout.write(char + " " + char)
                sys.stdout.flush()
                continue
            # Process the entered char
            char = char.decode()
            sys.stdout.write(char)
            sys.stdout.flush()
            string.append(char)
        # If char is non ASCII do nothing
        except:
            continue
    # We try to get message
    try:
        while True:
            cabecera_usuario = s.recv(HEADER)

            if not len(cabecera_usuario):  # No hay mensaje
                print('Se ha cerrado la conexión con el servidor')
                sys.exit()

            lon_msg = int(cabecera_usuario.decode().strip())
            msg = s.recv(lon_msg).decode()
            # Print received message, clean what's being written by client
            print('\r' + int(len(usuario)+2+len(string))*" " + '\r' + msg)
            # Print what client had written
            sys.stdout.write(usuario + ": " + ''.join(string))
            sys.stdout.flush()
    # Except can be message error or recv pause
    except:
        continue
s.close()
