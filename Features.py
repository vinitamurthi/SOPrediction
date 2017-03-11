
# coding: utf-8

# In[6]:

from bs4 import BeautifulSoup
import pandas as pd


# In[7]:

questions = pd.read_csv("input/TrainQuestions.csv", encoding='latin1')
answers = pd.read_csv("input/TrainAnswers.csv", encoding='latin1')
tags = pd.read_csv("input/TrainTags.csv", encoding='latin1')


# In[39]:

def feature(data):
    feat = [1]
    soup = BeautifulSoup(data['Body'],"lxml")
    numtags = len(set([tag.name for tag in soup.body.findAll(True)]))
    isimage = 1 if soup.body.findAll("img") else 0
    islink = 1 if soup.body.findAll("a") else 0
    iscode = 1 if (soup.body.findAll("code") or soup.body.findAll("pre")) else 0
    feat.extend([numtags,isimage,islink,iscode])
    return feat


# In[ ]:

X = [feature(questions.iloc[d]) for d in range(len(questions))]


# In[ ]:



