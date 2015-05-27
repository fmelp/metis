from pymongo import MongoClient
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import string
import re

client = MongoClient()
hmm = client.dsbc.hmm


################ CHALLENGE 1 #############
# Make a histogram of the years in the data.
# How many metal movies came out over the years?

years = []
# for i in xrange(hmm.count()):
#     cursor = hmm.find()
#     years.append(cursor.next()['year'])

cursor = hmm.find({})
years = []
for i in range(hmm.count()):
    years.append(cursor.next()['year'])

# sns.set_palette("deep", desat=.6)
# sns.set_context(rc={"figure.figsize": (8, 4)})

#run this for challenge 1
locs, labels = plt.xticks()
plt.setp(labels, rotation=90)
plt.hist(years, bins=len(set(years)))
plt.show()


################ CHALLENGE 2 #############
# Find the cast member that appeared in most Heavy Metal movies.
# Is there one that is shared by more than one of these movies?
# Or are they all completely different actors for every movie?

cursor = hmm.find({})
actor_dic = {}
for i in xrange(hmm.count()):
    cast = cursor.next()['cast']
    for actor in cast:
        if actor in actor_dic.keys():
            actor_dic[actor] += 1
        else:
            actor_dic[actor] = 1

z = [(i,actor_dic[i]) for i in actor_dic]
z.sort(key=lambda x: x[1], reverse=True)
print z ##answer
##alice cooper is in 15 movies! There's a fair amount of overlap of actors


################ CHALLENGE 3 #############
# Find the most used words in Heavy Metal film titles.
# Is there a word that appears in a lot of them? Is it "The"?
# If it is something like "the", How can you get around that?
# Find one "meaningful" word that appears the most
#         (this means non-structural word, unlike "the" or "a" or "in")


words = []
cursor = hmm.find()
for i in xrange(hmm.count()):
    title = cursor.next()['title'].lower()
    title_no_punc = re.sub(r'[^\w\s]', '', title).split()
    words.extend(title_no_punc)

stop_words = ["a", "i", "it", "am", "at", "on", "in", "to", "too", "very",
              "of", "from", "here", "even", "the", "but", "and", "is", "my",
              "them", "then", "this", "that", "than", "though", "so", "are"]
words_no_fillers = [str(word) for word in words if str(word) not in stop_words]
word_count = Counter(words_no_fillers)
print word_count
## metal: 36 times
## dead: 24 times
## rock: 19 times
## heavy: 19 times


################ CHALLENGE 4 #############
# METAL CRED section lists themes included in these movies that makes them more metal.
# What were the top 5 metal cred keywords in the 70s? In 80s? In 90s, In 2000s

s_cursor = hmm.find({'year':{ '$gte':1970, '$lt':1980} }, {'metal_cred':1, 'year':1, '_id':0})
seventies_cred = []
for i in s_cursor:
    seventies_cred.extend(i['metal_cred'][1:])
seventies_word_count = Counter(seventies_cred)
print seventies_word_count
# 1. Satan : 19
# 2. Black Mass : 10
# 3. Video Nasty : 7
# 4. Post-Apocalypse : 7
# 5. Zombies/Giallo : 6

e_cursor = hmm.find({'year':{ '$gte':1980, '$lt':1990} }, {'metal_cred':1, 'year':1, '_id':0})
eighties_cred = []
for i in e_cursor:
    eighties_cred.extend(i['metal_cred'][1:])
eighties_word_count = Counter(eighties_cred)
print eighties_word_count
# 'Post-Apocalypse': 29,
# 'Sword and Sorcery': 20,
# 'Satan': 16,
# 'Video Nasty': 12,
# Italian Horror': 11

n_cursor = hmm.find({'year':{ '$gte':1990, '$lt':2000} }, {'metal_cred':1, 'year':1, '_id':0})
nineties_cred = []
for i in n_cursor:
    nineties_cred.extend(i['metal_cred'][1:])
nineties_word_count = Counter(nineties_cred)
print nineties_word_count
#'Satan': 7,
# 'Gwar': 6,
# 'Post-Apocalypse': 4,
# 'Lemmy': 4,
# 'Zombies': 3


m_cursor = hmm.find({'year':{ '$gte':2000, '$lt':2016} }, {'metal_cred':1, 'year':1, '_id':0})
mill_cred = []
for i in m_cursor:
    mill_cred.extend(i['metal_cred'][1:])
mill_word_count = Counter(mill_cred)
print mill_word_count
#'Torture Porn': 14,
# 'Satan': 11,
# 'Christopher Lee': 7,
# 'Music Score: Charlie Clouser': 5,
# 'Billy Puppet': 5,
# 'Jigsaw': 5


################ CHALLENGE 5 #############
# Let's use the length of the METAL CRED section as a proxy score for how metal a movie is.
# Let's call this the METAL SCORE.
# To each mongo document, add the metal_score as a new field

cursor = hmm.find({}, {'metal_cred': 1, "_id":1})
# metal_cred_len = []
# for i in cursor:
#     metal_cred_len.append(len(i['metal_cred'][1:]))
## DONE IN PLACE HERE ##
for i in cursor:
    hmm.update({"_id": i["_id"]}, {"$set": {"metal_score": len(i['metal_cred'][1:])}})



################ CHALLENGE 6 #############
# Find the director that is MOST METAL per movie
#     (director with the highest average metal score).
# Remember that some movies have multiple directors.


cursor = hmm.find({}, {'metal_score': 1, "_id":0, "direct":1})
directd = {}
for i in cursor:
    for direct in i['direct']:
        if direct not in directd.keys():
            directd[direct] = [1, i['metal_score']]
        else:
            directd[direct][0] += 1
            directd[direct][1] += i['metal_score']
new_values = [x[1]/float(x[0]) for x in directd.values()]
new_d = dict(zip(directd.keys(), new_values))
print Counter(new_d)
# 'John Milius': 74.0,
# 'David Jacobson': 26.0,
# 'Robert Hendrickson': 17.0,
# 'Laurence Merrick': 17.0,
# 'Tinto Brass': 12.0,
# 'Bob Guccione': 12.0



################ CHALLENGE 7 #############
# The majority of directors and actors will have worked on a single movie.
# See if there are any directors that worked with an actor more than once.
# If so, find the director-actor duo that have worked together the most times.
cursor = hmm.find({}, {'cast': 1, "_id":0, "direct":1})
ad_pairs = {}
for i in cursor:
    for direct in i['direct']:
        for actor in i['cast']:
            pair = direct + ' + ' + actor
            if pair not in ad_pairs:
                ad_pairs[pair] = 1
            else:
                ad_pairs[pair] += 1
print Counter(ad_pairs)
# all these director actor pairs worked on 4 movies together
# 'Dario Argento + Daria Nicolodi': 4,
# 'Rob Zombie + Sheri Moon Zombie': 4,
# 'Joe D\u2019Amato + George Eastman': 4,
# 'Peter Jackson + Christopher Lee': 4



################ CHALLENGE 8 #############
# Create an index on the 'director' field to make the queries involving it faster
cursor = hmm.find({}, {'_id': 0, "direct": 1})
for i in cursor:
    hmm.create_index("direct")


################ CHALLENGE 9 #############
# For each decade, make a histogram of metal scores.
# Also, calculate the average metal score for each decade.
# Which decade was the most pure metal decade?

counter_70s = hmm.find({'year':{ '$gte':1970, '$lt':1980} }, {'metal_score':1, 'year':1, '_id':0})
scores_70s = []
for i in counter_70s:
    scores_70s.append(i['metal_score'])
avg_70s = sum(scores_70s)/float(len(scores_70s))
print avg_70s

counter_80s = hmm.find({'year':{ '$gte':1980, '$lt':1990} }, {'metal_score':1, 'year':1, '_id':0})
scores_80s = []
for i in counter_80s:
    scores_80s.append(i['metal_score'])
avg_80s = sum(scores_80s)/float(len(scores_80s))
print avg_80s

counter_90s = hmm.find({'year':{ '$gte':1990, '$lt':2000} }, {'metal_score':1, 'year':1, '_id':0})
scores_90s = []
for i in counter_90s:
    scores_90s.append(i['metal_score'])
avg_90s = sum(scores_90s)/float(len(scores_90s))
print avg_90s

counter_00s = hmm.find({'year':{ '$gte':2000, '$lt':2016} }, {'metal_score':1, 'year':1, '_id':0})
scores_00s = []
for i in counter_00s:
    scores_00s.append(i['metal_score'])
avg_00s = sum(scores_00s)/float(len(scores_00s))
print avg_00s

# 3.58125 -> so 70s is most pure metal decade
# 3.47386759582
# 2.78703703704
# 2.50643776824

plt.setp(labels, rotation=90)
plt.title("70s")
plt.hist(scores_70s, bins=len(set(scores_70s)))
plt.show()

plt.setp(labels, rotation=90)
plt.title("80s")
plt.hist(scores_80s, bins=len(set(scores_80s)))
plt.show()

plt.setp(labels, rotation=90)
plt.title("90s")
plt.hist(scores_90s, bins=len(set(scores_90s)))
plt.show()

plt.setp(labels, rotation=90)
plt.title("2000s")
plt.hist(scores_00s, bins=len(set(scores_00s)))
plt.show()




