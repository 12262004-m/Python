import socket
import sys
import json
import logging
from errors import IncorrectDataError
from files.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, RESPONDEFAULT_IP_ADDRESS
from files.utils import get_message, send_message
from decorator import log

SERVER_LOGGER = logging.getLogger('server')

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
    if '-p' in sys.argv:
        listen_port = int(sys.argv[sys.argv.index('-p') + 1])
    else:
        listen_port = DEFAULT_PORT
    if '-a' in sys.argv:
        listen_address = sys.argv[sys.argv.index('-a') + 1]
    else:
        listen_address = ''
    if listen_port < 1024 or listen_port > 65535:
        SERVER_LOGGER.critical(f'Ошибка. Неподходящий номер порта {listen_port}. Число не находится в диапазоне от 1024 до 65535')
        sys.exit(1)
    SERVER_LOGGER.info(f'Запущен сервер. Порт для подключений: {listen_port}, исходный адрес: {listen_address}')

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        SERVER_LOGGER.info('Установлено соедение с клиентом')
        try:
            message = get_message(client)
            SERVER_LOGGER.debug(f'Получено сообщение от клиента: {message}')
            response = client_message(message)
            SERVER_LOGGER.debug(f'Ответ клиенту: {response}')
            send_message(client, response)
            client.close()
        except json.JSONDecodeError:
            SERVER_LOGGER.error('Ошибка. Не удалось декодировать сообщение от клиента')
            client.close()
        except IncorrectDataError:
            SERVER_LOGGER.error('Ошика. От клиента получены некорректные данные')

if __name__ == '__main__':
    main()