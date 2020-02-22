# Dependencies
from bs4 import BeautifulSoup
import requests
import os
import re
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist

import pandas as pd
import numpy as np
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
nltk.download("stopwords")
nltk.download('punkt')
import scrape_mars 
import string


from importlib import reload

import sys
from imp import reload
import warnings
warnings.filterwarnings('ignore')
if sys.version[0] == '2':
   reload(sys)
#    sys.setdefaultencoding("utf-8")


nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer



from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Dense , Input , LSTM , Embedding, Dropout , Activation, GRU, Flatten
from keras.layers import Bidirectional, GlobalMaxPool1D
from keras.models import Model, Sequential
from keras.layers import Convolution1D
from keras import initializers, regularizers, constraints, optimizers, layers




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
    url5 = 'https://www.google.com/search?q=%23lightning'
    browser.visit(url5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # find tweet
    tweet5_info = soup.find("div", class_="xcQxib eadHV NdbWE YBEXSb")

    # get weather text
    lightning_text=tweet5_info.get_text("a")

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
    mars_data["lightning_tweets"] = lightning_text
    mars_data["earthquake_tweets"] = earthquake_text
    


     # Close the browser after scraping
    browser.quit()
     # Return results

    
    print(mars_data) 

    return mars_data



def clean_text(text):
    stop_words = set(stopwords.words("english")) 
    lemmatizer = WordNetLemmatizer()
    text = re.sub(r'[^\w\s]','',text, re.UNICODE)
    text = text.lower()
    text = [lemmatizer.lemmatize(token) for token in text.split(" ")]
    text = [lemmatizer.lemmatize(token, "v") for token in text]
    text = [word for word in text if not word in stop_words]
    text = " ".join(text)
    return text


def get_df():
    mars_data=scrape()
    data_values=[]
    for stuff in mars_data.values():
        data_values.append(stuff)

    df=pd.DataFrame(data_values)
    df.rename(columns={ df.columns[0]: "text" }, inplace = True)
    

    df['clean_text'] = df.text.apply(lambda x: clean_text(x))
    df.clean_text.apply(lambda x: len(x.split(" "))).mean() 

   
    print("CLEAN DATA")  
    return df



def prediction():
    df=get_df()

   
    
    model = pickle.load(open('02202020_model.sav', 'rb'))

    max_features = 6000
    tokenizer = Tokenizer(num_words=max_features)
    tokenizer.fit_on_texts(df['clean_text'])
    list_tokenized_train = tokenizer.texts_to_sequences(df['clean_text'])

    maxlen = 130
    X_t = pad_sequences(list_tokenized_train, maxlen=maxlen)



    list_sentences_test = df["clean_text"]
    list_tokenized_test = tokenizer.texts_to_sequences(list_sentences_test)
    X_te = pad_sequences(list_tokenized_test, maxlen=maxlen)
    predict = model.predict(X_te)
    y_pred = (predict > 0.5)

    y_values = y_pred[:,0].tolist()
    print ("##########################")

    true_disaster=[]
    d_true= "Yup -True"
    d_false= "Nope -False"

    for thing in y_values:
        if thing == True:
            true_disaster.append(d_true)
        else:
            true_disaster.append(d_false)


    tweet_data = df['text'].values.tolist()
    print (tweet_data)

    print("PREDICITONS HERE")
    print(y_pred)
    # keys=["prediction_1","prediction_2","prediction_3","prediction_4","prediction_5","prediction_6"]
    # tweetkeys= ["tweet_1","tweet_2","tweet_3","tweet_4","tweet_5","tweet_6"]
    
    prediction = dict(d_keys = true_disaster, tweetkeys = tweet_data)
    print (prediction)

       
    return prediction
    






  