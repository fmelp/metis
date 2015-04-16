from bs4 import BeautifulSoup as bs
from selenium import webdriver
import re


uastring = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36'


def search_movie(driver, movie_name):
    '''
    @param : driver -> selenium driver
             movie_name -> name of movie to search
    @return : movie_url_soup -> soup of imdb movie page
    '''
    search_url = "http://www.imdb.com/search/"
    imdb_url = "http://www.imdb.com"
    driver.get(search_url)
    driver.find_element_by_id('navbar-query').send_keys(movie_name)
    driver.find_element_by_id('navbar-submit-button').click()
    soup = bs(driver.page_source)
    div = soup.find(class_="findResult odd").find(class_="result_text")
    movie_url = imdb_url + str(div.a['href'])
    driver.get(movie_url)
    movie_url_soup = bs(driver.page_source)
    return movie_url_soup

def get_director(soup):
    try:
        director = str(soup.find(text=re.compile("Director:")).find_next('a').text)
        if director == ' \n':
            director = []
            director.append(str(soup.find(text=re.compile("Directors:")).find_next('a').text))
            director.append(str(soup.find(text=re.compile("Directors:")).find_next('a').find_next('a').text))
    except:
        director = None
    return director

def get_star_actors(soup):
    try:
        actors = []
        actors.append(str(soup.find(text=re.compile("Stars")).find_next('a').text))
        actors.append(str(soup.find(text=re.compile("Stars")).find_next('a').find_next('a').text))
        actors.append(str(soup.find(text=re.compile("Stars")).find_next('a').find_next('a').find_next('a').text))
    except:
        actors = None
    return actors


def get_genre(soup):
    '''
    @param : soup -> soup of movie imdb page

    @return : genres -> a list of genres
    '''
    try:
        divs = soup.find_all(itemprop="genre")
        div_wanted = len(divs) - 1
        str_to_parse = divs[div_wanted].text.encode("ascii", "ignore")
        genres = str_to_parse.split(" ")[1:]
        genres = [s.rstrip().rstrip("|") for s in genres]
    except:
        genres = None
    return genres


def get_ratings(soup):
    '''
    @param : soup -> soup of movie imdb page

    @return : imdb_rating -> imdb rating of given film
              metascore_rating -> metascore rating of given film
    '''
    try:
        imdb_rating = str(soup.find(itemprop="ratingValue").text)
        imdb_rating = imdb_rating.replace(".", "")
    except:
        imdb_rating = None
    try:
        metascore = soup.find(text=re.compile("Metascore")).findNextSibling()
        metascore_rating = str(metascore.text).strip().rstrip("/100")
    except:
        metascore_rating = None
    return imdb_rating, metascore_rating


if __name__ == '__main__':
    dcap = webdriver.DesiredCapabilities.PHANTOMJS
    dcap["phantomjs.page.settings.userAgent"] = uastring
    exec_path = '/usr/local/bin/phantomjs'
    driver = webdriver.PhantomJS(exec_path)
    driver.set_window_size(1024, 768)
    soup = search_movie(driver, "Return of the Living Dead 2")
    print get_ratings(soup)
