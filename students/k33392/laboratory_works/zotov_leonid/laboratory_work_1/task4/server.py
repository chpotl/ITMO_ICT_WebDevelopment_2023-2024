import socket
import threading

# Указываем адрес сервера и порт
server_address = ('localhost', 12345)

# Создаем серверный соксет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем соксет к адресу сервера
server_socket.bind(server_address)

# Начинаем слушать подключения
server_socket.listen(5)

clients = []


def handle_client(client_socket):
    while True:
        try:
            # Получаем сообщение от клиента и декодируем его
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            # Отправляем сообщение всем клиентам, кроме отправителя
            for client in clients:
                if client != client_socket:
                    client.send(message.encode('utf-8'))
        except:
            break

    # Удаляем клиента из списка и закрываем соединение
    clients.remove(client_socket)
    client_socket.close()


print("Server is on {}:{}".format(server_address[0], server_address[1]))

while True:
    # Принимаем входящее подключение
    client_socket, client_address = server_socket.accept()
    print("Connection from {}:{}".format(client_address[0], client_address[1]))

    # Добавляем клиента в список
    clients.append(client_socket)


    # Создаем и запускаем поток для обработки клиента
    client_thread = threading.Thread(
        target=handle_client, args=(client_socket,))
    client_thread.start()
