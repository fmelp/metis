import tmdbsimple as tmdb
import csv
import numpy as np

tmdb.API_KEY = '88e31b0e5a74132f460bdb6a0c26e0a4'


movie_data = []
with open("bom_data_w_rt_ratings.csv", "r") as bom_data:
    reader = csv.reader(bom_data)
    # skip header
    reader.next()
    for row in reader:
        movie_data.append(row)


for movie in movie_data:
    assert len(movie) == 16
    try:
        if movie[3] == 'N/A':
            movie_title = movie[0]
            search = tmdb.Search()
            search.movie(query=movie_title)
            movie_id = search.results[0]['id']
            response = tmdb.Movies(movie_id).info()
            budget = response['budget']
            if budget == 0: budget = np.NaN
            movie[3] = budget
        else:
            if '.' in movie[3]:
                movie[3] += '00000'
                movie[3] = movie[3].replace('.', '')
            else:
                movie[3] += '000000'
    except:
        print movie_title + " has no budget"
        if '.' in movie[3]:
            movie[3] += '00000'
            movie[3] = movie[3].replace('.', '')
        else:
            movie[3] += '000000'


with open("bom_data_w_rt_ratings_budget.csv", "w") as f:
    writer = csv.writer(f, delimiter=',')
    new_headers = ['movie_title', 'domestic_total_gross', 'runtime',
               'budget', 'release_date', 'distributor', 'genre',
               'actors', 'director', 'producers', 'rank_year',
               'rank_history', 'number_theaters', 'close_date',
               'rt_critics','rt_audience']
    writer.writerow(new_headers)
    for row in movie_data:
        writer.writerow(row)


# search = tmdb.Search()
# search.movie(query='Tales From the Darkside: The Movie')
# movie_id = search.results[0]['id']
# response = tmdb.Movies(movie_id).info()
# budget = response['budget']
# print budget
