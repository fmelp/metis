
import csv
from collections import OrderedDict
import dateutil.parser


with open("turnstile_150314.txt", "r") as turnstile_data:
    reader = csv.reader(turnstile_data)
    reader.next()  # gets rid of header
    keys = []
    values = []
    for row in reader:
        if tuple(row[:4]) not in keys:
            keys.append(tuple(row[:4]))
            values.append([row[4:]])
        else:
            values[keys.index(tuple(row[:4]))].append(row[4:])


def trim_fat(keys, values):
    for value in values:
        for i in xrange(len(value)):
            try:
                date = dateutil.parser.parse(value[i][2])
                entries = value[i][5].lstrip('0')
            except:
                date = 'N/A'
                entries = 'N/A'
            value[i] = [date, entries]
    return keys, values


def get_dates_counts_list(keys, values, index):
    one_turnstile = values[index]
    dates = []
    counts = []
    for i in xrange(len(one_turnstile)):
        dates.append(one_turnstile[i][0])
        counts.append(one_turnstile[i][1])
    return dates, counts


def compile_stations(keys, values):
    i = 0
    while i < len(values) - 2:
        station_one = keys[i][3]
        station_two = keys[i+1][3]
        if station_one == station_two:
            values[i] += values[i+1]
            del keys[i+1]
            del values[i+1]
        else:
            i += 1
    return keys, values


def combine_same_days(values, sign):
    for i, value in enumerate(values):
        d = {}
        for val in value:
            if val[0] not in d.keys():
                d[val[0]] = [val[1]]
            else:
                d[val[0]].append(val[1])
        temp = []
        d = OrderedDict(sorted(d.items(), key=lambda t: t[0]))
        for k, v in d.items():
            if v[0] == '':
                continue
            else:
                if sign == '+':
                    entries = sum(v)
                elif sign == '-':
                    entries = int(max(v)) - int(min(v))
                else:
                    assert sign == '+' or sign == '-', \
                        "wrong sign, need '+' or '-'"
                temp.append([k, entries])
        values[i] = temp
    return values


keys, values = trim_fat(keys, values)
values = combine_same_days(values, '-')
keys, values = compile_stations(keys, values)




print values[1]
