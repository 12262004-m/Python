import socket
import sys
import json
import logging
import argparse
import select
import time
from errors import IncorrectDataError
from files.variables import ACTION, ACCOUNT_NAME, SENDER, RESPONSE, MAX_CONNECTIONS, PRESENCE, TIME, USER, ERROR, RESPONDEFAULT_IP_ADDRESS, DEFAULT_PORT, MESSAGE, MESSAGE_TEXT
from files.utils import get_message, send_message
from decorator import log

SERVER_LOGGER = logging.getLogger('server')

@log
def process_client_message(message, messages_list, client):
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message and message[USER][ACCOUNT_NAME] == 'Гость':
        send_message(client, {RESPONSE: 200})
        return
    elif ACTION in message and message[ACTION] == MESSAGE and TIME in message and MESSAGE_TEXT in message:
        messages_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        return
    else:
        send_message(client, {
            RESPONSE: 400,
            ERROR: 'Ошибка'
        })
        return

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

@log
def client_message(message):
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента: {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message and message[USER][ACCOUNT_NAME] == 'Гость':
        return {RESPONSE: 200}
    return {
        RESPONDEFAULT_IP_ADDRESS: 400,
        ERROR: 'Ошибка'
    }

def main():
    listen_address, listen_port = parser()
    SERVER_LOGGER.info(f'Запущен сервер. Порт для подключений: {listen_port}, исходный адрес: {listen_address}')

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    clients = []
    messages = []
    transport.listen(MAX_CONNECTIONS)

    while True:
        try:
            client, client_address = transport.accept()
        except OSError as error:
            print(error.errno)
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

        if messages and send_list:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_list:
                try:
                    send_message(waiting_client, message)
                except:
                    SERVER_LOGGER.info(f'Клиент {waiting_client.getpeername()} отключился от сервера')
                    waiting_client.close()
                    clients.remove(waiting_client)

if __name__ == '__main__':
    main()