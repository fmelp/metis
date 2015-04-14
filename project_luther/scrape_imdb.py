from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re

uastring = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36'


def search_movie(driver, movie_name):
    '''
    @param : driver -> selenium driver
             movie_name -> name of movie to search
    @return : two strings : movie_url -> url of imdb page of movie_name
                            movie_business_url -> url of business page of movie_name
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
    soup = bs(driver.page_source)
    extension = str(soup.find(href=re.compile("/business"))['href'])
    movie_business_url = imdb_url + extension
    return movie_url, movie_business_url


if __name__ == '__main__':
    dcap = webdriver.DesiredCapabilities.PHANTOMJS
    dcap["phantomjs.page.settings.userAgent"] = uastring
    exec_path = '/usr/local/bin/phantomjs'
    driver = webdriver.PhantomJS(exec_path)
    driver.set_window_size(1024, 768)
