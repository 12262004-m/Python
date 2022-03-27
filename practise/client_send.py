import sys
import json
import socket
import time
import logging
import argparse
from files.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, SENDER, MESSAGE, MESSAGE_TEXT
from files.utils import get_message, send_message
from errors import MissingFieldError
from decorator import log

CLIENT_LOGGER = logging.getLogger('client')

@log
def message_from_server(message):
    if ACTION in message and message[ACTION] == MESSAGE and SENDER in message and MESSAGE_TEXT in message:
        print(f'Получено сообщение от пользователя {message[SENDER]}: \n {message[MESSAGE_TEXT]}')
        CLIENT_LOGGER.info(f'Получено сообщение от пользователя {message[SENDER]}: \n {message[MESSAGE_TEXT]}')
    else:
        CLIENT_LOGGER.error(f'Ошибка. Некорректное сообщение с сервера')


@log
def create_message(sock, account_name='Гость'):
    message = input('Введите сообщение для отправки или *Exit* для завершения работы: ')
    if message == 'Exit':
        sock.close()
        CLIENT_LOGGER.info('Завершение работы')
        print('До свидания!')
        sys.exit(0)
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }
    CLIENT_LOGGER.debug(f'Создан словарь сообщения: {message_dict}')
    return message_dict

@log
def create_presence(name = 'Гость'):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: name
        }
    }
    CLIENT_LOGGER.debug(f'Для пользователя {name} сформировано {PRESENCE} сообщение ')
    return out

@log
def process_answer(message):
    CLIENT_LOGGER.debug(f'Разбор сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE]:
            return 'OK'
        return message[ERROR]
    raise MissingFieldError(RESPONSE)

@log
def parser():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    argparser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    argparser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = argparser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode

    if not 1023 < server_port < 65536:
        CLIENT_LOGGER.critical(f'Ошибка. Неподходящий номер порта {server_port}. Число не находится в диапазоне от 1024 до 65535')
        sys.exit(1)

    if client_mode not in ('listen', 'send'):
        CLIENT_LOGGER.critical(f'Ошибка. Указан недопустимый режим работы {client_mode}')
        sys.exit(1)

    return server_address, server_port, client_mode

def main():
    server_address, server_port, client_mode = parser()
    if server_port < 1024 or server_port > 65535:
        CLIENT_LOGGER.critical(f'Ошибка. Неподходящий номер порта {server_port}. Число не находится в диапазоне от 1024 до 65535')
    CLIENT_LOGGER.info(f'Запущен клиент. Параметры: адрес: {server_address}, порт: {server_port}')

    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        message_to_server = create_presence()
        send_message(transport, message_to_server)
        answer = process_answer(get_message(transport))
        CLIENT_LOGGER.info(f'Ответ от сервера: {answer}')
        print(answer)
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Ошибка. Не удалось декодировать сообщение сервера')
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Ошибка при подключении к серверу {server_address}:{server_port}')
    except MissingFieldError as error:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле {error.missing_field}')
    else:
        if client_mode == 'send':
            print('Отправка сообщений.')
        else:
            print('Приём сообщений.')
        while True:
            if client_mode == 'send':
                try:
                    send_message(transport, create_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {server_address} было потеряно')
                    sys.exit(1)
            if client_mode == 'listen':
                try:
                    message_from_server(get_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {server_address} было потеряно')
                    sys.exit(1)

if __name__ == '__main__':
    main()