__author__ = 'Meng'
import nltk
from textblob import TextBlob
wiki = TextBlob("Python is a high-level, general-purpose programming language.")
# wiki.tags
# wiki.noun_phrases
testimonial = TextBlob("Textblob is amazingly simple to use. What great fun!")
# testimonial.sentiment
testimonial.sentiment.polarity

sample = TextBlob(FCompanyList[0].LeaderList[0].NewsList[1])
sample.sentiment.polarity
# sample.sentiment


def get_score(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

