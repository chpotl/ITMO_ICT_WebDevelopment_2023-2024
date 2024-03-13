import socket

server_address = ('localhost', 12345)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(server_address)

while True:
    try:
        a = float(input("Input cathets length: "))
        b = float(input("Input cathets length: "))

        client_socket.send(str(a).encode('utf-8'))
        client_socket.send(str(b).encode('utf-8'))

        result = client_socket.recv(1024).decode('utf-8')

        print("Hypotenuse: {}".format(result))
    except ValueError:
        print("Error: input number.")
    except Exception as e:
        print("Error: {}".format(e))
        break

client_socket.close()
