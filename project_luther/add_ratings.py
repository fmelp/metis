import csv
import ast
from rottentomatoes import RT
import time

#print RT('ny97sdcpqetasj8a4v2na8va').search('Don Juan de Marco')

movie_data = []
with open("bom_data_1980-2014.csv", "r") as bom_data:
    reader = csv.reader(bom_data)
    # skip header
    reader.next()
    for row in reader:
        movie_data.append(row)

for movie in movie_data:
    time.sleep(0.3)
    assert len(movie) == 14
    movie[1] = movie[1].replace("$", "").replace(",", "")
    movie[3] = movie[3].split(" ")[0].replace("$", "")
    movie[12] = movie[12].split(" ")[0].replace(',', '')
    if '[' in movie[6]:
      genre_list = ast.literal_eval(movie[6])
      movie[6] = genre_list[0]
    movie_title = movie[0]
    try:
        movie.append(RT('ny97sdcpqetasj8a4v2na8va').search(movie_title)[0]['ratings']['audience_score'])
        movie.append(RT('ny97sdcpqetasj8a4v2na8va').search(movie_title)[0]['ratings']['critics_score'])
    except:
        print movie_title + " not included"
        movie.extend(['', ''])


with open("bom_data_w_rt_ratings.csv", "w") as f:
    writer = csv.writer(f, delimiter=',')
    new_headers = ['movie_title', 'domestic_total_gross', 'runtime',
               'budget', 'release_date', 'distributor', 'genre',
               'actors', 'director', 'producers', 'rank_year',
               'rank_history', 'number_theaters', 'close_date',
               'rt_critics','rt_audience']
    writer.writerow(new_headers)
    for row in movie_data:
        writer.writerow(row)
