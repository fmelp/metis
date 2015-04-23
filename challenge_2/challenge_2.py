import pandas as pd

path_to_file = "/Users/francescomelpignano/Desktop/metis/challenge_2/2013_movies.csv"
data = pd.read_csv(path_to_file)

'''
Title,Budget,DomesticTotalGross,Director,Rating,Runtime,ReleaseDate
'''

#data = data.sort(columns = "domestic total gross", ascending = False)

dtg_time = data[["DomesticTotalGross", "Runtime"]]

print data

print dtg_time
