import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re

nltk.download('punkt')
nltk.download('stopwords')

# Import input file
df = pd.read_excel('input.xlsx')
df = df.iloc[0:150]
df.drop('URL_ID', axis=1, inplace=True)

# Extracting text from all the URLs
url_id = 1
data = []

for i in range(len(df)):
    url = df.iloc[i][0]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    content = soup.find(attrs={'class': 'td-post-content'})
    title = soup.find(attrs={'class': 'entry-title'})
    
    if content and title:
        content = content.text.replace('\xa0', ' ').replace('\n', ' ')
        title = title.text.replace('\n', ' ').replace('/', '')
        text = title + '. ' + content
        data.append(text)
        with open(f'{url_id}.txt', 'a') as f:
            f.write(text)
        url_id += 1

df1 = pd.Series(data)
df1.to_csv('output.csv', index=False)

# Read extracted files
text = pd.read_csv('150.txt', header=None)
text.drop(1, axis=1, inplace=True)
text = text.astype(str)

# Text processing functions
def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))

def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    return ' '.join([word for word in text.split() if word.lower() not in stop_words])

# Apply text processing functions
text[0] = text[0].apply(remove_punctuation)
text[0] = text[0].apply(remove_stopwords)

# Load stop words files
stop_words_files = [
    'StopWords_Auditor.txt',
    'StopWords_Currencies.txt',
    'StopWords_DatesandNumbers.txt',
    'StopWords_Generic.txt',
    'StopWords_GenericLong.txt',
    'StopWords_Geographic.txt',
    'StopWords_Names.txt'
]

stop_words = set(stopwords.words('english'))

for file in stop_words_files:
    stopwords_df = pd.read_csv(file, header=None)
    stopwords_df.columns = ['word']
    stopwords_df['word'] = stopwords_df['word'].apply(remove_punctuation)
    stopwords_df['word'] = stopwords_df['word'].apply(remove_stopwords)
    stop_words.update(set(stopwords_df['word']))

# Apply stop words removal
text[0] = text[0].apply(lambda x: ' '.join([word for word in x.split() if word.lower() not in stop_words]))

# Load positive and negative word lists
positive = pd.read_csv('positive-words.txt', header=None, names=['word'])
negative = pd.read_csv('negative-words.txt', header=None, names=['word'])

# Apply text processing to positive and negative word lists
positive['word'] = positive['word'].apply
