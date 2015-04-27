import csv
import ast
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import re
import numpy as np

uastring = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36'


movie_data = []
with open("final_data.csv", "r") as bom_data:
    reader = csv.reader(bom_data)
    # skip header
    reader.next()
    for row in reader:
        movie_data.append(row)


actors = []
for movie in movie_data:

    if '[' in movie[7]:
        actors.extend(ast.literal_eval(movie[7]))
    else:
        actors.extend(movie[7])


actors = list(set(actors))

for i,actor in enumerate(actors):
    actors[i] = actor.replace("(Cameo)","").replace("(Voice)","")
    if '*' in actor:
        act = actor.split("*")
        actors.extend(act)
        del actors[i]

actors = list(set(actors))


def get_kb_num(driver, actors):
    d = {}
    for actor in actors:
        try:
            search_url = "https://oracleofbacon.org"
            driver.get(search_url)
            driver.find_element_by_xpath("//*[@id='main']/form/table/tbody/tr/td/input[2]").send_keys(actor)
            driver.find_element_by_xpath("//*[@id='main']/form/table/tbody/tr/td/input[3]").click()
            soup = bs(driver.page_source)
            d[actor] = str(re.sub("[^0-9]", "", soup.find(text=re.compile("Bacon number"))))
        except:
            d[actor] = np.nan
        print d[actor], actor
    return d





if __name__ == '__main__':
    dcap = webdriver.DesiredCapabilities.PHANTOMJS
    dcap["phantomjs.page.settings.userAgent"] = uastring
    exec_path = '/usr/local/bin/phantomjs'
    driver = webdriver.PhantomJS(exec_path)
    driver.set_window_size(1024, 768)
    d = get_kb_num(driver, actors)
