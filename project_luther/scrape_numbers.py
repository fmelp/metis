from bs4 import BeautifulSoup as bs
from selenium import webdriver
import re

print 'a'


def search_movie_numbers(movie_name):
    '''
    @param : movie_name -> name of movie to search
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
        rt_critics = str(soup.find(text=re.compile("Certified Fresh|Fresh|")))
        rt_critics = rt_critics.partition("%")[0]
        rt_audience = str(soup.find(text=re.compile("Upright")))
        rt_audience = rt_audience.partition("%")[0]
    except:
        rt_critics, rt_audience = None, None
    return rt_critics, rt_audience


if __name__ == '__main__':
    url = search_movie_numbers("avatar")
    print get_video_sales(url)
    print get_rt_ratings(url)