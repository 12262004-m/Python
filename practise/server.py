import socket
import sys
import json
import logging
import argparse
import select
import time
from errors import IncorrectDataError
from files.variables import ACTION, ACCOUNT_NAME, SENDER, RESPONSE, DESTINATION, MAX_CONNECTIONS, PRESENCE, RESPONSE_400, RESPONSE_200, TIME, USER, ERROR, RESPONDEFAULT_IP_ADDRESS, DEFAULT_PORT, MESSAGE, MESSAGE_TEXT
from files.utils import get_message, send_message
from decorator import log

SERVER_LOGGER = logging.getLogger('server')

@log
def process_client_message(message, messages_list, client, clients, names):
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message:
        if message[USER][ACCOUNT_NAME] not in names.keys():
            names[message[USER][ACCOUNT_NAME]] = client
            send_message(client, RESPONSE_200)
        else:
            response = RESPONSE_400
            response[ERROR] = 'Имя пользователя уже занято'
            send_message(client, response)
            clients.remove(client)
            client.close()
        return
    elif ACTION in message and message[ACTION] == MESSAGE and SENDER in message and DESTINATION in message and TIME in message and MESSAGE_TEXT in message:
        messages_list.append(message)
        return
    else:
        response = RESPONSE_400
        response[ERROR] = 'Запрос некорректен'
        send_message(client, response)
        return

@log
def process_message(message, names, listen_socks):
    if message[DESTINATION] in names and names[message[DESTINATION]] in listen_socks:
        send_message(names[message[DESTINATION]], message)
        SERVER_LOGGER.info(f'Отправлено сообщение пользователю {message[DESTINATION]} от пользователя {message[SENDER]}')
    elif message[DESTINATION] in names and names[message[DESTINATION]] not in listen_socks:
        raise ConnectionError
    else:
        SERVER_LOGGER.error(
            f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере')


@log
def parser():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    argparser.add_argument('-a', default='', type=str, nargs='?')
    namespace = argparser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    if not 1023 < listen_port < 65536:
        SERVER_LOGGER.critical(f'Ошибка. Неподходящий номер порта {listen_port}. Число не находится в диапазоне от 1024 до 65535')
        sys.exit(1)
    return listen_address, listen_port

def main():
    listen_address, listen_port = parser()
    SERVER_LOGGER.info(f'Запущен сервер. Порт для подключений: {listen_port}, исходный адрес: {listen_address}')

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    transport.bind((listen_address, listen_port))
    transport.settimeout(0.5)
    clients = []
    messages = []
    names = dict()
    transport.listen(MAX_CONNECTIONS)


    while True:
        try:
            client, client_address = transport.accept()
        except OSError:
            pass
        else:
            SERVER_LOGGER.info('Установлено соедение с клиентом')
            clients.append(client)
        recieve_list = []
        send_list = []
        error_lst = []
        try:
            if clients:
                recieve_list, send_list, error_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        if recieve_list:
            for client_with_message in recieve_list:
                try:
                    process_client_message(get_message(client_with_message), messages, client_with_message)
                except:
                    SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} отключился от сервера')
                clients.remove(client_with_message)

        for i in messages:
            try:
                process_message(i, names, send_list)
            except Exception:
                SERVER_LOGGER.info(f'Связь с клиентом с именем {i[DESTINATION]} была потеряна')
                clients.remove(names[i[DESTINATION]])
                del names[i[DESTINATION]]
        messages.clear()

if __name__ == '__main__':
    main()