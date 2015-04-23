import csv
import ast
from rottentomatoes import RT

print RT('ny97sdcpqetasj8a4v2na8va').search('avatar')[0]['ratings']

movie_data = []
with open("fuller_data_by_line_v1.csv", "r") as bom_data:
    reader = csv.reader(bom_data)
    # skip header
    reader.next()
    for row in reader:
        movie_data.append(row)

del movie_data[len(movie_data)-1]

genres = []

for movie in movie_data:
    assert len(movie) == 19
    movie[1] = movie[1].replace("$", "").replace(",", "")
    movie[3] = movie[3].split(" ")[0].replace("$", "")
    movie[12] = movie[12].split(" ")[0].replace(',', '')
    if '[' in movie[6]:
      genre_list = ast.literal_eval(movie[6])
      movie[6] = genre_list[0]
    if genre_list[0] not in genres:
      genres.append(genre_list[0])



with open("fixed_fuller_data_by_line_v1.csv", "w") as f:
    writer = csv.writer(f, delimiter=',')
    new_headers = ['movie_title', 'domestic_total_gross', 'runtime',
               'budget', 'release_date', 'distributor', 'genre',
               'actors', 'director', 'producers', 'rank_year',
               'rank_history', 'number_theaters', 'close_date',
               'imdb_rating', 'metascore_rating', 'rt_critics',
               'rt_audience', 'video_sales']
    writer.writerow(new_headers)
    for row in movie_data:
        writer.writerow(row)

print len(genres)