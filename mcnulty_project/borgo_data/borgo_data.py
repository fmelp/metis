import pandas as pd
import numpy as np
import re
from vincent import *
from pyzipcode import ZipCodeDatabase

# bd = pd.read_csv("~/Desktop/Ospiti.csv", skiprows=[248, 471, 1515,
#                                                    1614, 1816, 3478,
#                                                    3940, 3942])

bd = pd.read_csv("~/Desktop/metis/mcnulty_project/borgo_data/Ospiti.csv", sep=';')

# transform zipcodes
bd['CAP'] = bd['CAP'].dropna().apply(lambda x: re.sub("[^0-9]", "", x)).apply(lambda x: x if len(x) == 5 else np.nan)

# keep only well-formatted zip code
#   457 elements
bd = bd[bd['CAP'] != np.nan]
bd = bd[~(bd['CAP'].isnull())]


# .state, .zip, .longitude, .latitude, .city
zcdb = ZipCodeDatabase()
# print zcdb[22060].longitude

# uncomment below section to get list ready for us_map html viz
# city_number = {}
# for zc in bd['CAP']:
#     try:
#         city = zcdb[zc].city
#     except:
#         continue
#     if (city in city_number):
#         city_number[city] = city_number[city] + 1
#     else:
#         city_number[city] = 1
# for key in city_number:
#     print ("[ '" + str(key) + "', " + str(city_number[key]) + "],")

# 430 valid zipcodes

zp = pd.read_csv("~/Desktop/metis/mcnulty_project/borgo_data/zip-income-census.csv")
zp1 = pd.read_csv("~/Desktop/metis/mcnulty_project/borgo_data/zip-income.csv")
#zp1 = pd.read_csv("~/Desktop/metis/mcnulty_project/borgo_data/irs2.csv")



print len(zp)
print len(zp1)


zip_income_d = {}
for index, row in zp1.iterrows():
    zip_income_d[row['zipcode']] = row['mean_household_income']

my_zip_income_d = {}
for z in bd['CAP']:
    if int(z) in zip_income_d:
        my_zip_income_d[z] = zip_income_d[int(z)]
print my_zip_income_d
print len(my_zip_income_d)

# remove already used zips
for index, row in zp1.iterrows():
    if str(row['zipcode']) in my_zip_income_d.keys():
        zp1.index.delete(row)

zp1 = zp1[(zp1['mean_household_income'] > 180000)]
print len(zp1)
zips = zp1['zipcode'].tolist()

new_zips = [x for x in zips if str(x) not in my_zip_income_d.keys()]
print len(new_zips)

print len(my_zip_income_d.keys())
print sum([my_zip_income_d[key] for key in my_zip_income_d])/len(my_zip_income_d)
