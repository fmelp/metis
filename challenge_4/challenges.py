import csv
import pandas as pd
import numpy as np

pd.options.mode.chained_assignment = None

# def read_data(filename):
#     '''
#     @param -> filename : name of file to process (no header)
#     @return -> data : list where each element is a list of info from each line
#     '''
#     data = []
#     with open(filename, 'r') as f:
#         reader = csv.reader(f)
#         for row in reader:
#             data.append(row)
#     return data

# data = read_data("house-votes-84.csv")

data = pd.read_csv("~/Desktop/metis/challenge_4/house-votes-84.csv")


# for index, row in data.iterrows():
#     row.apply(lambda x: 1 if x == 'y')
#     row.apply(lambda x: 0 if x == 'n')

# print data.head()

data.replace(to_replace={'y':1, 'x':0})