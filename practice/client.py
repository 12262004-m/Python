import sys
import json
import socket
import time
import logging
from files.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from files.utils import get_message, send_message
from errors import MissingFieldError

CLIENT_LOGGER = logging.getLogger('client')

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

def process_answer(message):
    CLIENT_LOGGER.debug(f'Разбор сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE]:
            return 'OK'
        return message[ERROR]
    raise MissingFieldError(RESPONSE)

def main():
    server_address = sys.argv[1]
    server_port = int(sys.argv[2])
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

if __name__ == '__main__':
    main()