from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import csv
import scrape_imdb


new_headers = ['movie_title', 'domestic_total_gross', 'runtime',
           'budget', 'release_date', 'distributor', 'genre',
           'actors', 'director', 'producers', 'rank_year',
           'rank_history', 'number_theaters', 'close_date',
           'imdb_rating', 'metascore_rating', 'rt_critics',
           'rt_audience', 'video_sales']


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



def fill_missing_data(movie_data):
    with open("fuller_data_by_line_post_1989.csv", "w") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(new_headers)
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
                writer.writerow(movie)
            except:
                print "nothing was appended to " + str(movie[0])
        return movie_data


if __name__ == '__main__':
    dcap = webdriver.DesiredCapabilities.PHANTOMJS
    dcap["phantomjs.page.settings.userAgent"] = uastring
    exec_path = '/usr/local/bin/phantomjs'
    driver = webdriver.PhantomJS(exec_path)
    driver.set_window_size(1024, 768)
    print "starting..."
    movie_data = fill_missing_data(movie_data[864:])