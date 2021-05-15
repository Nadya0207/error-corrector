import re
import json
import csv


def delete_extra(data):
    for i in data.values():
        for k in range(len(i[0]['from_user']) - 1):
            if i[0]['from_user'][k] == i[0]['from_user'][k + 1]:
                i[0]['from_user'].pop(k)
    return data


def delete_matches(data):
    for i in data.values():
        for k in range(min((len(i[0]['from_user']) - 1), (len(i[1]['from_bot']) - 1))):
            if i[0]['from_user'][k]['text'] == i[1]['from_bot'][k]['text']:
                i[0]['from_user'].pop(k)
                i[1]['from_bot'].pop(k)
    return data


def tokenizator(data):
    token_from_user = []
    token_from_bot = []
    for i in data.values():
        for k in i[0]['from_user']:
            s = k['text'].replace('ё', 'е')
            a = re.findall(r'[А-ЯA-Za-zа-я]+', s)
            token_from_user.append(a)
        for k1 in i[1]['from_bot']:
            s1 = k1['text'].replace('ё', 'е')
            b = re.findall(r'[А-ЯA-Za-zа-я]+', s1)
            token_from_bot.append(b)
    token_from_all = dict()
    for j in range(len(token_from_bot)):
        for j1 in range(len(token_from_user)):
            if j == j1:
                for r in range(len(token_from_bot[j])):
                    for r1 in range(len(token_from_user[j1])):
                        if r == r1:
                            token_from_all[token_from_bot[j][r]] = token_from_user[j1][r1]
    return token_from_all


def match_token(token):
    token_selected = dict()
    for i in token.keys():
        if i == token[i]:
            None
        else:
            token_selected[i] = token[i]
    return token_selected


def ready_data(data):
    return match_token(tokenizator(delete_matches(delete_extra(data))))


with open('data_from_bot.json', 'r', encoding='utf-8') as f:
    memory_from_bot = json.load(f)

with open('data_from_user.json', 'r', encoding='utf-8') as f1:
    memory_from_user = json.load(f1)

memory_all = dict()

for key_1 in memory_from_bot.keys():
    for key_2 in memory_from_user.keys():
        if key_1 == key_2:
            memory_all[key_1] = [{'from_user': memory_from_user[key_1]}, {'from_bot': memory_from_bot[key_2]}]


with open('data.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter=';', lineterminator='\n')
    for i in range(len(ready_data(memory_all))):
        writer.writerow([list(ready_data(memory_all))[i], str(list(ready_data(memory_all).values())[i])])
        print([list(ready_data(memory_all))[i], str(list(ready_data(memory_all).values())[i])])
