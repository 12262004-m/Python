import csv
import re
import chardet
"""«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы»"""


def get_data():
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data = []

    for i in range(1, 4):
        with open(f'info_{i}.txt', 'rb') as file:
            content = file.read()
            result = chardet.detect(content)
            data = content.decode(result['encoding'])

        os_prod_info = re.compile(r'Изготовитель системы:\s*\S*')
        os_prod_list.append(os_prod_info.findall(data)[0].split()[2])

        os_name_info = re.compile(r'Windows\s\S*')
        os_name_list.append(os_name_info.findall(data)[0])

        os_code_info = re.compile(r'Код продукта:\s*\S*')
        os_code_list.append(os_code_info.findall(data)[0].split()[2])

        os_type_info = re.compile(r'Тип системы:\s*\S*')
        os_type_list.append(os_type_info.findall(data)[0].split()[2])

    headings = ["Изготовитель системы", "Название ОС", "Код продукта", "Тип системы"]
    main_data.append(headings)
    data_for_rows = [os_prod_list, os_name_list, os_code_list, os_type_list]
    for j in range(len(data_for_rows[0])):
        row = [line[j] for line in data_for_rows]
        main_data.append(row)

    return main_data

def write_to_csv(new_file):
    main_data = get_data()
    with open(new_file, 'w', encoding='utf-8') as f_n:
        f_n_writer = csv.writer(f_n)
        for row in main_data:
            f_n_writer.writerow(row)

write_to_csv('data_report.csv')