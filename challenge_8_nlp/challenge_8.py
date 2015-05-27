import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from nltk.corpus import stopwords
import re


# Challenge 1
# Calculate the tf-idf for each word in the first 100
#         reviews in the nltk movie reviews corpus.
# For each document, print the top 10 tf-idf words.

def fix_reviews(text):
    letters_only = re.sub("[^a-zA-Z]", " ", text)
    words = letters_only.lower().split()
    stops = set(stopwords.words("english"))
    meaningful_words = [w for w in words if not w in stops]
    return( " ".join( meaningful_words ))


fileids = movie_reviews.fileids()[:100]
doc_words = [movie_reviews.words(fileid) for fileid in fileids]
documents = [' '.join(words) for words in doc_words]
for i in xrange(len(documents)):
    documents[i] = fix_reviews(documents[i])


vectorizer = TfidfVectorizer(stop_words="english")
doc_vectors = vectorizer.fit_transform(documents)

for doc in doc_words:
    d = dict(zip(doc, ))
