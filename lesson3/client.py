import sys
import json
import socket
import time
from files.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from files.utils import get_message, send_message

def create_presence(name = 'Гость'):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: name
        }
    }
    return out

def process_answer(message):
    if RESPONSE in message:
        if message[RESPONSE]:
            return 'OK'
        return message[ERROR]
    raise ValueError

def main():
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        print('Ошибка. Число не находится в диапазоне от 1024 до 65535')
        sys.exit(1)

        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        message_to_server = create_presence()
        send_message(transport, message_to_server)
        try:
            answer = process_answer(get_message(transport))
            print(answer)
        except (ValueError, json.JSONDecodeError):
            print('Ошибка. Не удалось декодировать сообщение сервера')

if __name__ == '__main__':
    main()