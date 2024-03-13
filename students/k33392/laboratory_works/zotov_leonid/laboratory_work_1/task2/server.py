import socket

server_address = ('localhost', 12345)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(server_address)

server_socket.listen(1)

print("Server is on {}:{}".format(server_address[0], server_address[1]))


def calculate_hypotenuse(a, b):
    return (a ** 2 + b ** 2) ** 0.5


while True:
    client_socket, client_address = server_socket.accept()
    print("Connection from {}:{}".format(client_address[0], client_address[1]))

    try:
        a = float(client_socket.recv(1024).decode('utf-8'))
        b = float(client_socket.recv(1024).decode('utf-8'))

        result = calculate_hypotenuse(a, b)

        client_socket.send(str(result).encode('utf-8'))
    except ValueError:
        client_socket.send("Error: wrong data.".encode('utf-8'))
    except:
        client_socket.send(
            "Error: couldn't handle response.".encode('utf-8'))

    client_socket.close()
