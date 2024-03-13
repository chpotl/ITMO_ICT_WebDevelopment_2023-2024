import socket

# Указываем адрес сервера и порт
server_address = ('localhost', 8080)


while True:
    try:
        # Создаем клиентский соксет
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Устанавливаем соединение с сервером
        client_socket.connect(server_address)
        # Запрашиваем у пользователя название дисциплины
        discipline = input(
            "Введите название дисциплины (или 'exit' для выхода): ")
        # Если пользователь ввел 'exit', выходим из цикла
        if discipline.lower() == 'exit':
            break
        # Запрашиваем оценку у пользователя
        grade = input("Введите оценку: ")

        # Формируем POST-запрос для отправки на сервер
        post_request = "POST / HTTP/1.1\r\n" # Задаем начало POST-запроса, указываем метод, путь и версию протокола
        post_request += "Host: {}\r\n".format(server_address[0]) # Указываем заголовок Host с адресом сервера
        post_request += "Content-Type: application/x-www-form-urlencoded\r\n" # Устанавливаем тип содержимого как форма
        post_request += "Content-Length: {}\r\n\r\n".format(
            len("discipline={}&grade={}".format(discipline, grade))) # Указываем длину тела запроса
        post_request += "discipline={}&grade={}".format(discipline, grade) # Добавляем тело запроса с данными о дисциплине и оценке

        # Отправляем POST-запрос на сервер
        client_socket.send(post_request.encode('utf-8'))

        # Получаем и выводим ответ от сервера
        response = client_socket.recv(1024).decode('utf-8')
        print(response)
    except Exception as e:
        # В случае ошибки выводим сообщение об ошибке
        print("Ошибка: {}".format(e))

client_socket.close()
