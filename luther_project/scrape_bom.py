from bs4 import BeautifulSoup as bs
from selenium import webdriver
import re
import csv
import time
import random

uastring = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36'
search_url = 'http://www.imdb.com/find?ref_=nv_sr_fn&q=&s=all'


def get_movie_value(soup, field_name):
    """
    takes a string attribute of a movie on the page
    returns the string in the next sibling object (the value for that attribute)
    """
    obj = soup.find(text=re.compile(field_name))
    if not obj:  # can use assert as well
        return None
    next_sibling = obj.findNextSibling()
    if next_sibling:
        return str(next_sibling.text)
    else:
        return None

def get_movie_roles_list(soup, role):
    try:
        obj = soup.find(text=re.compile(role))
        if not obj:
            return None
        obj = str(soup.find(text=re.compile(role)).next()[0].text)
        obj = re.split('([a-z](?=[A-Z]))', obj)
        for i, x in enumerate(obj):
            if len(x) == 1:
                obj[i-1] = obj[i-1] + obj[i]
                del obj[i]
    except:
        obj = None
    return obj


def get_hard_vals(soup, value):
    try:
        obj = soup.find(text=re.compile(value))
        if not obj:
            return None
        next_elem = obj.find_next('td')
        obj = next_elem.text.encode("ascii", "ignore")
    except:
        obj = None
    return obj


def get_all_movie_links(driver, start_year, end_year):
    year_links = []
    all_links = []
    count = 0
    for year in xrange(start_year, end_year + 1):
        year_links.append("http://www.boxofficemojo.com/yearly/chart/?yr="
                          + str(year) + "&p=.htm")
    for year_link in year_links:
        driver.get(year_link)
        soup = bs(driver.page_source)
        movies_from_year = soup.find_all('a', href=re.compile("/movies"))
        assert len(movies_from_year) == 103, "This page has inconsistent formatting"
        # take only from indicies 2-101
        movies_from_year = movies_from_year[2:102]
        for i in xrange(len(movies_from_year)):
            try:
                all_links.append("http://www.boxofficemojo.com" +
    				             str(movies_from_year[i]['href']))
            except UnicodeError:
                count += 1
    # notify user how many movies not included in final list
    print str(count) + " movies impropely formatted and not included in all_links"
    assert len(all_links) == (end_year - start_year + 1) * 100 - count
    return all_links


def get_movie_info(all_links):
    movie_data = []
    headers = ["movie title", "domestic total gross", "runtime",
                   "budget", "release date", "distributor", "genre",
                   "actors", "director", "producers", "rank in year",
                   "rank in history", "number of theaters", "close date"]
    movie_data.append(headers)
    for link in all_links:
        time.sleep(random.uniform(0, 1))
        driver.get(link)
        soup = bs(driver.page_source)
        title_string = soup.find("title").text
        title = str(title_string.split("(")[0].strip())
        dtg = get_movie_value(soup, "Domestic")
        runtime = get_movie_value(soup, "Runtime")
        budget = get_movie_value(soup, "Production Budget")
        release_date = get_movie_value(soup, "Release Date")
        distributor = get_movie_value(soup, "Distributor")
        genre = get_movie_value(soup, "Genre:")
        actors = get_movie_roles_list(soup, "Actors")
        director = get_movie_roles_list(soup, "Director")
        producers = get_movie_roles_list(soup, "Producer")
        year_rank = rank = get_hard_vals(soup, "Yearly ")
        rank = get_hard_vals(soup, "All Time Domestic")
        num_theaters = get_hard_vals(soup, "Widest\xa0Release")
        close_date = get_hard_vals(soup, "Close\xa0Date")
        row = [title, dtg, runtime, budget, release_date,
               distributor, genre, actors, director, producers,
               year_rank, rank, num_theaters, close_date]
        movie_data.append(row)
        # if None in row:
        #     print title + " has incomplete data"
        if not dtg:
            print "------ " + title + " has no earnings -------"
        print row
    return movie_data


def write_to_csv(movie_data):
    with open("bom_data.csv", "w") as f:
        writer = csv.writer(f, delimiter=',')
        for row in movie_data:
            writer.writerow(row)
        print "movie data written to bom_data.csv"


if __name__ == '__main__':
    dcap = webdriver.DesiredCapabilities.PHANTOMJS
    dcap["phantomjs.page.settings.userAgent"] = uastring
    exec_path = '/usr/local/bin/phantomjs'
    driver = webdriver.PhantomJS(exec_path)
    driver.set_window_size(1024, 768)
    movie_data = get_movie_info(get_all_movie_links(driver, 1980, 2014))
    write_to_csv(movie_data)
