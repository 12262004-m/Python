import subprocess
import chardet

args_yandex = ['ping', 'yandex.ru']
result_1 = subprocess.Popen(args_yandex, stdout=subprocess.PIPE)
for line in result_1.stdout:
    result_1 = chardet.detect(line)
    line = line.decode(result_1['encoding']).encode('utf-8')
    print(line.decode('utf-8'))

args_youtube = ['ping', 'youtube.com']
result_2 = subprocess.Popen(args_youtube, stdout=subprocess.PIPE)
for line in result_2.stdout:
    result_2 = chardet.detect(line)
    line = line.decode(result_2['encoding']).encode('utf-8')
    print(line.decode('utf-8'))