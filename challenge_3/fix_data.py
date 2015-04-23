import csv

movie_data = []
with open("fuller_data_1980_2014.csv", "r") as bom_data:
    reader = csv.reader(bom_data)
    # skip header
    reader.next()
    for row in reader:
        movie_data.append(row)

for movie in movie_data:
    movie[1] = movie[1].replace("$", "").replace(",", "")
    movie[3] = movie[3].split(" ")[0].replace("$", "")
    movie[12] = movie[12].split(" ")[0].replace(',', '')


with open("fixed_1980_2014.csv", "w") as f:
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
