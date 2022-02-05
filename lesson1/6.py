from chardet import detect

f = open('test_file.txt', 'w', encoding='utf-8')
f.write('сетевое программирование\nсокет\nдекоратор')
f.close()

with open('test_file.txt', 'rb') as f:
    content = f.read()
encoding = detect(content)['encoding']

with open('test_file.txt', encoding=encoding) as f_1:
    for elem in f_1:
        print(elem, end='')