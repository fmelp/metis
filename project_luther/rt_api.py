from bs4 import BeautifulSoup as bs
import urllib2

movie_data = []
with open("bom_data_1980-2014.csv", "r") as bom_data:
    reader = csv.reader(bom_data)
    # skip header
    reader.next()
    for row in reader:
        movie_data.append(row)

def get_movie_info(movie_data):
    movie_name =
    url = 'http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey=v2wgmxsk7we5cts5u5p3uysb&q=Toy+Story+3&page_limit=1'
    url.
