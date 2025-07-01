PPC (Professional Programming and Coding) - соревнование по решению интерактивных задач.

Задача располагается на сервере (выполняется в удаленном терминале) и доступна по команде

nc ip-adress port

однако решить ее в "ручном режиме" не представляется возможным из-за ограничений времени ответа и/или большого количества повторений.

Типичная ситуация - необходимо реализовать перехват данных с некоторого порта и быстро реагировать на содержание этих данных.

Как быть с такими задачами? Подключаемся к серверу, получаем от него данные на свой компьютер, решаем задачу, отправляем ответ и т.д., пока не получим флаг. Флаги наши - в формате grodno{0-9a-zA-Z!+-}

from time import sleep
import socket

sock = socket.socket()
sock.connect(("ip-adress", port))

while True:
    sleep(1)
   # получить данные от сервера
    data = sock.recv(1024).decode('utf-8')
   # проверить, может там уже флаг ?
    if 'grodno{' in data:
        print(data)
        break
    task = f1(data) # извлечь условие задачи из data
    result = f2(task) # вычислить ответ
   # отправить ответ
    sock.send((str(result) + '\r\n').encode())

sock.close()

Если все понятно - введите флаг 0

PPC (Professional Programming and Coding) - a competition to solve interactive problems.

The task is located on the server (executed in a remote terminal) and is available using the command

nc ip-adress port

however, it is not possible to solve it “manually” due to limitations in response time and/or the large number of repetitions.

A typical situation is that it is necessary to intercept data from a certain port and quickly respond to the content of this data.

How to deal with such tasks? We connect to the server, receive data from it on our computer, solve the problem, send a response, etc., until we receive the flag. Our flags are in the format grodno{0-9a-zA-Z!+-}

from time import sleep
import socket

sock = socket.socket()
sock.connect(("ip-adress", port))

while True:
     sleep(1)
    # get data from server
     data = sock.recv(1024).decode('utf-8')
    # check if there is already a flag there?
     if 'grodno{' in data:
         print(data)
         break
     task = f1(data) # extract task condition from data
     result = f2(task) # calculate the answer
    # send reply
     sock.send((str(result) + '\r\n').encode())

sock.close()

If everything is clear, enter the flag 0
