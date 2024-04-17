from config import ROOT_DIR
import json
import datetime
import os


def jet_json_data(path):
    """
    Получает список транзакций и сортирует по дате.
    """
    with open(path) as json_data:
        data = []
        for i in json.load(json_data):
            if i != {}:
                date_time = datetime.datetime.strptime(i['date'][0:10], '%Y-%m-%d')
                date_correct = date_time.strftime('%d.%m.%Y')
                i['date'] = date_correct
                data.append(i)
        data.sort(key=lambda item: (datetime.datetime.strptime(item['date'], '%d.%m.%Y')), reverse=True)
        return data


def jet_last_executed():
    """
    Оставляет только 5 последних успешных операций
    с замаскированными счетами.
    """
    last_executed = []
    FILE_PATH = os.path.join(ROOT_DIR, 'json_data', 'operations.json')
    for i in jet_json_data(FILE_PATH):
        if i['state'] == 'EXECUTED':
            if i['description'] != 'Открытие вклада':
                if 'Счет' not in i['from']:
                    i['from'] = f"{i['from'][:-12]} {i['from'][-12:-10]}** **** {i['from'][-4:]}"
                    i['to'] = f"{i['to'][:-20]}**{i['to'][-5:-1]}"
                    last_executed.append(i)
                if 'Счет' in i['from']:
                    i['from'] = f"{i['from'][:-20]}**{i['from'][-4:]}"
                    i['to'] = f"{i['to'][:-20]}**{i['to'][-5:-1]}"
                    last_executed.append(i)
            if i['description'] == 'Открытие вклада':
                i['to'] = f"{i['to'][:-20]}**{i['to'][-5:-1]}"
                last_executed.append(i)
    return last_executed[0:5]


def output_last_operations():
    """
    Выводит результат в соответствующем формате
    """
    output = []
    for i in jet_last_executed():
        if i['description'] != 'Открытие вклада':
            output.append(f"{i['date']} {i['description']}\n"
                          f"{i['from']} -> {i['to']}\n"
                          f"{i['operationAmount']['amount']} {i['operationAmount']['currency']['name']}\n")
        else:
            output.append(f"{i['date']} {i['description']}\n"
                          f"{i['to']}\n")
    return output
