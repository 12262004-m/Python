import sys
import json
import socket
import time
import argparse
import logging
import print_helper
import threading
from files.variables import ACTION, PRESENCE, DESTINATION, TIME, EXIT, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, SENDER, MESSAGE, MESSAGE_TEXT
from files.utils import get_message, send_message
from errors import MissingFieldError, IncorrectDataError, ServerError
from decorator import log
from practice.client import print_help

CLIENT_LOGGER = logging.getLogger('client')

@log
def create_exit_message(account_name):
    return {
        ACTION: EXIT,
        TIME: time.time(),
        ACCOUNT_NAME: account_name
    }


@log
def message_from_server(sock, my_username):
    while True:
        try:
            message = get_message(sock)
            if ACTION in message and message[ACTION] == MESSAGE and DESTINATION in message and SENDER in message and MESSAGE_TEXT in message and message[DESTINATION] == my_username:
                print(f'Получено сообщение от пользователя {message[SENDER]}: \n {message[MESSAGE_TEXT]}')
                CLIENT_LOGGER.info(f'Получено сообщение от пользователя {message[SENDER]}: \n {message[MESSAGE_TEXT]}')
            else:
                CLIENT_LOGGER.error(f'Ошибка. Некорректное сообщение с сервера')
        except IncorrectDataError:
            CLIENT_LOGGER.error(f'Не удалось декодировать полученное сообщение.')
        except (OSError, ConnectionError, ConnectionAbortedError,
                ConnectionResetError, json.JSONDecodeError):
            CLIENT_LOGGER.critical(f'Потеряно соединение с сервером.')
            break


@log
def create_message(sock, account_name='Гость'):
    to_user = input('Введите получателя сообщения: ')
    message = input('Введите сообщение для отправки или *Exit* для завершения работы: ')
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }
    CLIENT_LOGGER.debug(f'Создан словарь сообщения: {message_dict}')
    try:
        send_message(sock, message_dict)
        CLIENT_LOGGER.info(f'Отправлено сообщение для пользователя {to_user}')
    except Exception as e:
        print(e)
        CLIENT_LOGGER.critical('Потеряно соединение с сервером.')
        sys.exit(1)

@log
def user_interactive(sock, username):
    print_help()
    while True:
        command = input('Введите команду: ')
        if command == 'message':
            create_message(sock, username)
        elif command == 'help':
            print_help()
        elif command == 'exit':
            send_message(sock, create_exit_message(username))
            print('Завершение соединения.')
            CLIENT_LOGGER.info('Завершение работы по команде пользователя.')
            time.sleep(0.5)
            break
        else:
            print('ОШибка. Попробойте снова. help - вывести поддерживаемые команды.')

def print_help():
    print('Команды:')
    print('message - отправить сообщение')
    print('help - вывести подсказки по командам')
    print('exit - выход из программы')

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
    print(f'Консольный месседжер. Клиентский модуль. Имя пользователя: {client_mode}')
    if not client_mode:
        client_mode = input('Введите имя пользователя: ')
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
        sys.exit(1)
    except ServerError as error:
        CLIENT_LOGGER.error(f'При установке соединения сервер вернул ошибку: {error.text}')
        sys.exit(1)
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Ошибка при подключении к серверу {server_address}:{server_port}')
        sys.exit(1)
    except MissingFieldError as error:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле {error.missing_field}')
        sys.exit(1)
    else:
        receiver = threading.Thread(target=message_from_server, args=(transport, client_mode))
        receiver.daemon = True
        receiver.start()

        user_interface = threading.Thread(target=user_interactive, args=(transport, client_mode))
        user_interface.daemon = True
        user_interface.start()
        CLIENT_LOGGER.debug('Запущены процессы')

        while True:
            time.sleep(1)
            if receiver.is_alive() and user_interface.is_alive():
                continue
            break
if __name__ == '__main__':
    main()