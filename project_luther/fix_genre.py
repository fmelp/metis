import csv

movie_data = []
with open("final_data.csv", "r") as bom_data:
    reader = csv.reader(bom_data)
    # skip header
    reader.next()
    for row in reader:
        movie_data.append(row)

print movie_data[3]


# for movie in movie_data:
#     if movie[6]:
#         movie[6] = movie[6].split()[0]
#     if movie[6] == 'Unknown':
#         movie[6] = np.nan


# with open("final_data_genre.csv", "w") as f:
#     writer = csv.writer(f, delimiter=',')
#     new_headers = ['movie_title', 'domestic_total_gross', 'runtime',
#                'budget', 'release_date', 'distributor', 'genre',
#                'actors', 'director', 'producers', 'rank_year',
#                'rank_history', 'number_theaters', 'close_date',
#                'imdb_rating', 'metascore_rating', 'rt_critics',
#                'rt_audience', 'video_sales']
#     writer.writerow(new_headers)
#     for row in movie_data:
#         writer.writerow(row)