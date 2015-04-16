from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import csv
import scrape_imdb
import scrape_numbers
import pprint



uastring = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36'

movie_data = []
with open("bom_data_1980-2014.csv", "r") as bom_data:
    reader = csv.reader(bom_data)
    # skip header
    reader.next()
    for row in reader:
        movie_data.append(row)


def fill_missing_data_from_imdb(movie_data):
    for movie in movie_data:
        try:
            idmb_soup = scrape_imdb.search_movie(driver, movie[0])
            # fill missing directors
            if movie[8] == '':
                movie[8] = scrape_imdb.get_director(idmb_soup)
            # replace genre if imdb_genre not none
            new_genre = scrape_imdb.get_genre(idmb_soup)
            if new_genre:
                movie[6] = new_genre
            # replace actors if imdb_genre not none
            new_actors = scrape_imdb.get_star_actors(idmb_soup)
            if new_actors:
                movie[7] = new_actors
            # add imdb rating
            imdb_rating, metascore_rating = scrape_imdb.get_ratings(idmb_soup)
            movie.append(imdb_rating)
            movie.append(metascore_rating)
        except:
            movie.extend(['', ''])
    return movie_data


def fill_missing_data_from_numbers(movie_data):
    for movie in movie_data:
        try:
            # add rotten tomatoes ratings (audience and critics)
            numbers_url = scrape_numbers.search_movie_numbers(driver, movie[0])
            print type(numbers_url)
            rt_crit, rt_aud = scrape_numbers.get_rt_ratings(numbers_url)
            movie.append(rt_crit)
            movie.append(rt_aud)
            print rt_crit, rt_aud
            # add video sales
            video_sales = scrape_numbers.get_video_sales(numbers_url)
            movie.append(video_sales)
        except:
            movie.extend(['', '', ''])
    return movie_data


def write_to_csv(movie_data):
    with open("fuller_data.csv", "w") as f:
        writer = csv.writer(f, delimiter=',')
        new_headers = ['movie title', 'domestic total gross', 'runtime',
                   'budget', 'release date', 'distributor', 'genre',
                   'actors', 'director', 'producers', 'rank in year',
                   'rank in history', 'number of theaters', 'close date',
                   'imdb rating', 'metascore rating', 'rt critics',
                   'rt audience', 'video sales']
        writer.writerow(new_headers)
        for row in movie_data:
            writer.writerow(row)
        print "movie data written to fuller_data.csv"


if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    dcap = webdriver.DesiredCapabilities.PHANTOMJS
    dcap["phantomjs.page.settings.userAgent"] = uastring
    exec_path = '/usr/local/bin/phantomjs'
    driver = webdriver.PhantomJS(exec_path)
    driver.set_window_size(1024, 768)
    print "starting..."
    movie_data = fill_missing_data_from_imdb(movie_data)
    movie_data = fill_missing_data_from_numbers(movie_data)
    write_to_csv(movie_data)
