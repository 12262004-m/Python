import json

def write_order_to_json(item, quantity, price, buyer, date):
    with open("orders.json", "r", encoding="utf-8") as f_out:
        content = json.load(f_out)

    with open("orders.json", "w", encoding="utf-8") as f_in:
        orders_list = content['orders']
        order = {
            'item': item,
            'quantity': quantity,
            'price': price,
            'buyer': buyer,
            'date': date
        }
        orders_list.append(order)
        json.dump(content, f_in, indent=4, ensure_ascii=False)

write_order_to_json('computer', '2', '87000', 'Jacob Smith', '13.02.2022')
write_order_to_json('принтер', '5', '32000', 'Иванов Иван Иванович', '11.01.2021')