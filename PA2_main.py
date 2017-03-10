
# coding: utf-8

# In[1]:

import collections
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
get_ipython().magic('matplotlib inline')
import math
import string
from bs4 import BeautifulSoup
import nltk
#from nltk import tokenize


# In[2]:

questions = pd.read_csv("Questions.csv", encoding='latin1')
answers = pd.read_csv("Answers.csv", encoding='latin1')
tags = pd.read_csv("Tags.csv", encoding='latin1')


# In[3]:

print(len(questions))
questions.iloc[[0]]


# In[39]:

text = questions.ix[98]['Body']
soup = BeautifulSoup(text, 'lxml')
allCode = soup.body.findAll("code")
text_filtered = soup.getText()


# In[5]:

answers[answers['ParentId']==80]


# In[6]:

tags.iloc[[0]]


# In[7]:

idxs = np.random.choice(range(1264216),200000)

considered_questions= questions.iloc[idxs]
considered_questions.to_csv("TrainQuestions.csv")
print(len(considered_questions))

considered_answers = answers[answers['ParentId'].isin(considered_questions['Id'])]
print(len(considered_answers))

considered_answers.to_csv("TrainAnswers.csv")
considered_tags = tags[tags['Id'].isin(considered_questions['Id'])]
print(len(considered_tags))

considered_tags.to_csv("TrainTags.csv")


# In[34]:

with open('en_US.txt') as f:
    en_dict = set(f.read().splitlines())
with open('en_US2.txt') as f:
    en_dict = en_dict.union(set(f.read().splitlines()))
with open('programmingDict.txt') as f:
    en_dict = en_dict.union(set(f.read().splitlines()))


# In[9]:

def filter_code_links(soup):
    
    link= soup.a
    while link is not None:
        link.replace_with("link")
        link = link.code

    code = soup.code
    while code is not None:
        code.replace_with("code")
        code = soup.code
        
    return soup.getText()



# In[57]:

def count_spell_errors(text):
    sentences = nltk.sent_tokenize(text)
    error_count = 0
    for s in sentences:
        if s[0].islower():
            error_count += 1
        r = ''.join([c for c in s if not c in punctuation])
        words = r.split()
        word = words[0]
        if word not in en_dict and word.lower() not in en_dict:
            if word not in prog_dict and word.lower() not in prog_dict:
#                print(word)
                error_count+=1
        for w in words[1:]:
            if w not in en_dict:
                if w not in prog_dict:
#                    print(w)
                    error_count+=1
    return error_count


# In[68]:

def get_length_error(soup):
    text = filter_code_links(soup)
    error_ct = count_spell_errors(text)
    length = len(text)
    error_ratio = error_ct*1.0/length
    return length, error_ratio


# In[58]:

text_filtered = filter_code_links(soup)
print(text_filtered)


# In[59]:

punctuation = set(['.',',',';',':','(',')','!','?','\"'])
print(count_spell_errors(text_filtered))


# In[70]:

def feature(data):
    feat = [1]
     
    soup_title = BeautifulSoup(data['Title'],"lxml")
    soup_body = BeautifulSoup(data['Body'],"lxml")
    
    numtags = len(set([tag.name for tag in soup.body.findAll(True)]))
    isimage = 1 if soup.body.findAll("img") else 0
    islink = 1 if soup.body.findAll("a") else 0
    
    code_length = 0
    allCode = soup.body.findAll("code")
    if allCode:
        iscode = 1
        for code in allCode:
            code_length += len(str(code).split())
    else:
        iscode = 0
    
    body_length, error_ratio_body = get_length_error(soup_body)
    title_length, error_ratio_title = get_length_error(soup_title)
    
    feat.extend([numtags,isimage,islink,iscode, code_length, title_length, error_ratio_title, body_length, error_ratio_body])
    return feat







