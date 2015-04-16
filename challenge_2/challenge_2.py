import pandas as pd

path_to_file = "/Users/francescomelpignano/Desktop/metis/project_luther/bom_data_1980-2014.csv"
data = pd.read_csv(path_to_file)

#data = data.sort(columns = "domestic total gross", ascending = False)

print data[['domestic total gross', 'movie title']]
