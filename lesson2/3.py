import yaml

data_for_file = {
    'workers_list': ['Иванов И.И', 'Попова А.А', 'Сидоров Н.Н', 'Козлов С.С', 'Петрова Л.Л'],
    'amount': 5,
    'salaries': {'Иванов И.И': '750$',
                 'Попова А.А': '1200$',
                 'Сидоров Н.Н': '486$',
                 'Козлов С.С': '892$',
                 'Петрова Л.Л': '681$'}
}

with open('file.yaml', 'w') as f_in:
    yaml.dump(data_for_file, f_in, default_flow_style=False, allow_unicode=True)

with open('file.yaml', 'r') as f_out:
    data_in_file = yaml.load(f_out, Loader=yaml.SafeLoader)

print(data_for_file == data_in_file)