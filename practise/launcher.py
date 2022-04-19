import subprocess

PROCESS = []
while True:
    ACTION = input('Выберите действие: quit - выйти, start - запустить сервер и клиенты, finish - закрыть все окна: ')
    if ACTION == 'quit':
        break
    elif ACTION == 'start':
        PROCESS.append(subprocess.Popen('python server.py',
                                          creationflags=subprocess.CREATE_NEW_CONSOLE))
        PROCESS.append(subprocess.Popen('python client.py -n test1',
                                          creationflags=subprocess.CREATE_NEW_CONSOLE))
        PROCESS.append(subprocess.Popen('python client.py -n test2',
                                          creationflags=subprocess.CREATE_NEW_CONSOLE))
        PROCESS.append(subprocess.Popen('python client.py -n test3',
                                          creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif ACTION == 'finish':
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.kill()