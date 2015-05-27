import csv

l=[]
with open("movie_data.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        l.append(row)

print l
