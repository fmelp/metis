from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import csv
import scrape_imdb


def search_movie_numbers(movie_name):
    '''
    @param : driver -> selenium driver
             movie_name -> name of movie to search
    @return : movie_url -> url of the_numbers movie page
    '''
    uastring = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36'
    dcap = webdriver.DesiredCapabilities.PHANTOMJS
    dcap["phantomjs.page.settings.userAgent"] = uastring
    exec_path = '/usr/local/bin/phantomjs'
    driver = webdriver.PhantomJS(exec_path)
    driver.set_window_size(1024, 768)
    url = "http://www.the-numbers.com/search?searchterm="
    movie_name = movie_name.replace(" ", "+")
    url = url + movie_name
    driver.get(url)
    xpath = '//*[@id="page_filling_chart"]/center/table/tbody/tr[2]/td[3]/b/a'
  #  driver.save_screenshot("a.png")
    driver.find_element_by_xpath(xpath).click()
    return str(driver.current_url)

def get_video_sales(url):
    '''
    @param : url -> the_numbers url for the given movie
    @return : video_sales -> string of video sales
    '''
    try:
        driver.get(url)
        xpath = '//*[@id="movie_finances"]/tbody/tr[8]/td[2]'
        video_sales = str(driver.find_element_by_xpath(xpath).text)
    except:
        try:
            xpath = '//*[@id="movie_finances"]/tbody/tr[7]/td[2]'
            video_sales = str(driver.find_element_by_xpath(xpath).text)
        except:
            video_sales = None
    return video_sales

def get_rt_ratings(url):
    '''
    @param : url -> the_numbers url for the given movie
    @return : rt_critics -> string of rotten tomatoes critics rating
              rt_audience -> string of rotten tomatoes audience rating
    '''
    try:
        driver.get(url)
        soup = bs(driver.page_source)
        rt_critics = str(soup.find(text=re.compile("- Certified Fresh|- Fresh|- Rotten")))
        rt_critics = rt_critics.partition("%")[0]
        rt_audience = str(soup.find(text=re.compile("- Upright|- Spilled")))
        rt_audience = rt_audience.partition("%")[0]
    except:
        rt_critics, rt_audience = None, None
    return rt_critics, rt_audience


uastring = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36'

movie_data = []
with open("bom_data_1980-2014.csv", "r") as bom_data:
    reader = csv.reader(bom_data)
    # skip header
    reader.next()
    for row in reader:
        movie_data.append(row)


# def fill_missing_data_from_imdb(movie_data):
#     for movie in movie_data:
#         try:
#             idmb_soup = scrape_imdb.search_movie(driver, movie[0])
#             # fill missing directors
#             if movie[8] == '':
#                 movie[8] = scrape_imdb.get_director(idmb_soup)
#             # replace genre if imdb_genre not none
#             new_genre = scrape_imdb.get_genre(idmb_soup)
#             if new_genre:
#                 movie[6] = new_genre
#             # replace actors if imdb_genre not none
#             new_actors = scrape_imdb.get_star_actors(idmb_soup)
#             if new_actors:
#                 movie[7] = new_actors
#             # add imdb rating
#             imdb_rating, metascore_rating = scrape_imdb.get_ratings(idmb_soup)
#             movie.append(imdb_rating)
#             movie.append(metascore_rating)
#         except:
#             movie.extend(['', ''])
#     return movie_data


# def fill_missing_data_from_numbers(movie_data):
#     for movie in movie_data:
#         try:
#             # add rotten tomatoes ratings (audience and critics)
#             numbers_url = scrape_numbers.search_movie_numbers(driver, movie[0])
#             print type(numbers_url)
#             rt_crit, rt_aud = scrape_numbers.get_rt_ratings(numbers_url)
#             movie.append(rt_crit)
#             movie.append(rt_aud)
#             print rt_crit, rt_aud
#             # add video sales
#             video_sales = scrape_numbers.get_video_sales(numbers_url)
#             movie.append(video_sales)
#         except:
#             movie.extend(['', '', ''])
#         print movie
#     return movie_data

def prevent_timeout():
    """Create a function that ends the current loop when it's taking too long.
    To use: run this function, then put @timeout() before the loop you need to
    advance in case of a timeout.

    This is useful for if a server returns something unusual that makes a
    loop infinite for some reason, or if the server goes into some weird
    extended lag, or if the internet cuts out and then cuts back in again
    (which could cause unexpected script behavior)."""

    from functools import wraps
    import errno, os, signal
    class TimeoutError(Exception):
        pass

    def timeout(seconds = 15, error_message = os.strerror(errno.ETIME)):
        def decorator(func):
            def _handle_timeout(signum, frame):
                raise TimeoutError(error_message)

            def wrapper(*args, **kwargs):
                signal.signal(signal.SIGALRM, _handle_timeout)
                signal.alarm(seconds)
                try:
                    result = func(*args, **kwargs)
                finally:
                    signal.alarm(0)
                return result

            return wraps(func)(wrapper)

        return decorator

def fill_missing_data(movie_data):
    reload(scrape_imdb)
    for movie in movie_data:
        movie.extend(['', '', '', '', ''])
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
            movie[14] = imdb_rating
            movie[15] = metascore_rating

            url = search_movie_numbers(movie[0])
            rt_crit, rt_aud = get_rt_ratings(url)
            movie[16] = rt_crit
            movie[17] = rt_aud
            video_sales = get_video_sales(url)
            movie[18] = video_sales
            print movie[0], imdb_rating, metascore_rating, rt_crit, rt_aud, video_sales
            print movie
        except:
            print "nothing was appended to " + str(movie[0])
    return movie_data



def write_to_csv(movie_data):
    with open("fuller_data.csv", "w") as f:
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
        print "movie data written to fuller_data.csv"


if __name__ == '__main__':
    dcap = webdriver.DesiredCapabilities.PHANTOMJS
    dcap["phantomjs.page.settings.userAgent"] = uastring
    exec_path = '/usr/local/bin/phantomjs'
    driver = webdriver.PhantomJS(exec_path)
    driver.set_window_size(1024, 768)
    print "starting..."
    movie_data = fill_missing_data(movie_data)
    write_to_csv(movie_data)
