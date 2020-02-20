# import pickle
# from flask_pymongo import PyMongo
# import os
# import re
# import nltk
# import numpy as np
# import pandas as pd
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from nltk.stem.porter import PorterStemmer
# nltk.download("stopwords")
# nltk.download('punkt')
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.feature_extraction.text import TfidfVectorizer
# import scrape_mars 
# import string
# from xgboost import XGBClassifier


# def find_hashtags(tweet):
#     return " ".join([match.group(0)[1:] for match in re.finditer(r"#\w+", tweet)]) or 'no'
# def find_mentions(tweet):
#     return " ".join([match.group(0)[1:] for match in re.finditer(r"@\w+", tweet)]) or 'no'
# def find_links(tweet):
#     return " ".join([match.group(0)[:] for match in re.finditer(r"https?://\S+", tweet)]) or 'no'
# def tolkencleaner(text):
#     stop_words = set(stopwords.words('english'))
#     punctuation = set(string.punctuation)
#     ps = PorterStemmer()
#     tolkenized = []
#     no_link = re.sub(r'https?://\S+', '', text)
#     no_break = re.sub(r'\n',' ', no_link)
#     cleaner = re.sub('\s+', ' ', no_break).strip()
#     word_tokens = word_tokenize(cleaner)
#     stripped = [ps.stem(w) for w in word_tokens if not w in punctuation]
#     split_sentence = [w for w in stripped if not w in stop_words]
#     filtered_sentence = [w.lower() for w in split_sentence]
#     finished_sentence = ' '.join(filtered_sentence)
#     tolkenized.append(finished_sentence)
#     df = pd.DataFrame(tolkenized, columns=['text'])
#     df['hashtag'] = df['text'].apply(lambda x: find_hashtags(x))
#     df['mentions'] = df['text'].apply(lambda x: find_mentions(x))
#     df['links'] = df['text'].apply(lambda x: find_links(x))
#     print(df)
#     return df

# def vectorizing(df):
#     cv_hashtag = CountVectorizer()
#     cv_mentions = CountVectorizer()
#     cv_link = CountVectorizer(analyzer = 'word', token_pattern = r'https?://\S+')
#     ht = cv_hashtag.fit_transform(df['hashtag'])
#     mt = cv_mentions.fit_transform(df['mentions'])
#     lt = cv_link.fit_transform(df['links'])
#     print("look herererererererrer", ht, mt, lt)
#     train_ht = pd.DataFrame(ht.toarray(), columns=cv_hashtag.get_feature_names())
#     train_mt = pd.DataFrame(mt.toarray(), columns=cv_mentions.get_feature_names())
#     train_lt = pd.DataFrame(lt.toarray(), columns=cv_link.get_feature_names())
#     print("look herererererererrer", train_ht, train_mt, train_lt)
#     vec_text = TfidfVectorizer(min_df = 10, ngram_range = (1,2)) 
#     vt = vec_text.fit_transform(df['tolkenized'])
#     print("look herererererererrer",vt)
#     train_txt = pd.DataFrame(vt.toarray(), columns=vec_text.get_feature_names())
#     T = pd.DataFrame(train_txt)
#     T = T.join(train_ht, rsuffix='_link')
#     T = T.join(train_lt, rsuffix='_hashtags')
#     T = T.join(train_mt, rsuffix='_mentions')
#     print(T)
#     return T


# def prediction():

#     mars_app = mongo.db.mars_app
#     mars_data = mars_app.mars_data
    
#     # vectorizing = vectorizing()
#     # tolkencleaner = tolkencleaner()
#     clf = pickle.load(open('finalized_model.sav', 'rb'))

#     prediction=[]

#     for tweet in mars_data.values():
#         try:
#             label = {0:'negative', 1:'positive'}
#             d = tolkencleaner(tweet)
#             X = vectorizing(d)
#             print('Prediction: %s\nProbability: %.2f%%' %\
#                 (label[clf.predict(X)[0]], 
#                 np.max(clf.predict_proba(X))*100))
        
#             prediction=  (label[clf.predict(X)[0]], np.max(clf.predict_proba(X))*100)
#             print(prediction)
#         except Exception:
#             pass
    
#     return prediction