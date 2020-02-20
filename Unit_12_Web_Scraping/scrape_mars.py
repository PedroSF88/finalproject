# Dependencies
from bs4 import BeautifulSoup
import requests
import os
import re
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
nltk.download("stopwords")
nltk.download('punkt')
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import scrape_mars 
import string
from xgboost import XGBClassifier


def init_browser():
    #chromium path 
    chromiumPath=r'C:/Users/floPe/OneDrive/Desktop/chromedriver.exe'
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": chromiumPath}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # Scraper 3  Tweet

#### find fire tweets
    #https://twitter.com/marswxreport?lang=en for Tweet

    url1 = 'https://www.google.com/search?q=%23fire'
    browser.visit(url1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # find tweet
    tweet_info = soup.find("div", class_="xcQxib eadHV NdbWE YBEXSb")

    # get weather text
    fire_text=tweet_info.get_text("a")

### find flood tweets
    url2 = 'https://www.google.com/search?q=%23flood'
    browser.visit(url2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # find tweet
    tweet2_info = soup.find("div", class_="xcQxib eadHV NdbWE YBEXSb")

    # get weather text
    flood_text=tweet2_info.get_text("a")


##### find storm tweets
    url3 = 'https://www.google.com/search?q=%23storm'
    browser.visit(url3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # find tweet
    tweet3_info = soup.find("div", class_="xcQxib eadHV NdbWE YBEXSb")

    # get weather text
    storm_text=tweet3_info.get_text("a")

##### find disaster tweets
    url4 = 'https://www.google.com/search?q=%23disaster'
    browser.visit(url4)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # find tweet
    tweet4_info = soup.find("div", class_="xcQxib eadHV NdbWE YBEXSb")

    # get weather text
    disaster_text=tweet4_info.get_text("a")

##### find blaze tweets
    url5 = 'https://www.google.com/search?q=%23thunder'
    browser.visit(url5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # find tweet
    tweet5_info = soup.find("div", class_="xcQxib eadHV NdbWE YBEXSb")

    # get weather text
    thunder_text=tweet5_info.get_text("a")

##### find earthquake tweets
    url6 = 'https://www.google.com/search?q=%23earthquake'
    browser.visit(url6)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # find tweet
    tweet6_info = soup.find("div", class_="xcQxib eadHV NdbWE YBEXSb")

    # get weather text
    earthquake_text=tweet6_info.get_text("a")




   # Store data in a dictionary
    mars_data={}
   
    

    mars_data["fire_tweets"] = fire_text
    mars_data["flood_tweets"] = flood_text
    mars_data["storm_tweets"] = storm_text
    mars_data["disaster_tweets"] = disaster_text
    mars_data["thunder_tweets"] = thunder_text
    mars_data["earthquake_tweets"] = earthquake_text
    


     # Close the browser after scraping
    browser.quit()
     # Return results

    
    print(mars_data) 

    return mars_data



def find_hashtags(tweet):
    return " ".join([match.group(0)[1:] for match in re.finditer(r"#\w+", tweet)]) or 'no'
def find_mentions(tweet):
    return " ".join([match.group(0)[1:] for match in re.finditer(r"@\w+", tweet)]) or 'no'
def find_links(tweet):
    return " ".join([match.group(0)[:] for match in re.finditer(r"https?://\S+", tweet)]) or 'no'
def tolkencleaner(text):
    stop_words = set(stopwords.words('english'))
    punctuation = set(string.punctuation)
    ps = PorterStemmer()
    tolkenized = []
    no_link = re.sub(r'https?://\S+', '', text)
    no_break = re.sub(r'\n',' ', no_link)
    cleaner = re.sub('\s+', ' ', no_break).strip()
    word_tokens = word_tokenize(cleaner)
    stripped = [ps.stem(w) for w in word_tokens if not w in punctuation]
    split_sentence = [w for w in stripped if not w in stop_words]
    filtered_sentence = [w.lower() for w in split_sentence]
    finished_sentence = ' '.join(filtered_sentence)
    tolkenized.append(finished_sentence)
    df = pd.DataFrame(tolkenized, columns=['text'])
    df['hashtag'] = df['text'].apply(lambda x: find_hashtags(x))
    df['mentions'] = df['text'].apply(lambda x: find_mentions(x))
    df['links'] = df['text'].apply(lambda x: find_links(x))
    return df

def vectorizing(df):
    cv_hashtag = CountVectorizer()
    cv_mentions = CountVectorizer()
    ht = cv_hashtag.fit_transform(df['hashtag'])
    mt = cv_mentions.fit_transform(df['mentions'])
    train_ht = pd.DataFrame(ht.toarray(), columns=cv_hashtag.get_feature_names())
    train_mt = pd.DataFrame(mt.toarray(), columns=cv_mentions.get_feature_names())
    vec_text = TfidfVectorizer(ngram_range = (1,2)) 
    vt = vec_text.fit_transform(df['text'])
    train_txt = pd.DataFrame(vt.toarray(), columns=vec_text.get_feature_names())
    T = pd.DataFrame(train_txt)
    T = T.join(train_ht, rsuffix='_hashtags')
    T = T.join(train_mt, rsuffix='_mentions')
    print(T)
    return T


def prediction():
    mars_data=scrape()
    # mars_data
    # vectorizing = vectorizing()
    # tolkencleaner = tolkencleaner()
    clf = pickle.load(open('finalized_model.sav', 'rb'))
    tweets = {}
    num = 0
    for tweet in mars_data.values():
        num += 1
        label = {0:'negative', 1:'positive'}
        d = tolkencleaner(tweet)
        X = vectorizing(d)
        print('Prediction: %s\nProbability: %.2f%%' %\
            (label[clf.predict(X)[0]], 
            np.max(clf.predict_proba(X))*100))
        
        tweets[num] = (label[clf.predict(X)[0]], np.max(clf.predict_proba(X))*100)

    return tweets






  