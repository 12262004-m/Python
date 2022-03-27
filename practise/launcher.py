import subprocess

PROCESS = []
while True:
    ACTION = input('Выберите действие: quit - выйти, start - запустить сервер и клиенты, finish - закрыть все окна: ')
    if ACTION == 'quit':
        break
    elif ACTION == 'start':
        PROCESS.append(subprocess.Popen('python server.py', creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(2):
            PROCESS.append(subprocess.Popen('python client.py -m send', creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(2):
            PROCESS.append(subprocess.Popen('python client.py -m listen', creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif ACTION == 'finish':
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.kill()