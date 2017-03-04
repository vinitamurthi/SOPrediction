
# coding: utf-8

# In[3]:

import collections
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
get_ipython().magic('matplotlib inline')
import math


# In[5]:

questions = pd.read_csv("input_full/Questions.csv", encoding='latin1')
answers = pd.read_csv("input_full/Answers.csv", encoding='latin1')
tags = pd.read_csv("input_full/Tags.csv", encoding='latin1')


# In[6]:

print(len(questions))
questions.iloc[[0]]


# In[7]:


answers.iloc[[0]]


# In[8]:

tags.iloc[[0]]


# In[9]:

answers[answers['ParentId']==80]


# In[10]:

idxs = np.random.choice(range(1264216),200000)
print(idxs)
considered_questions= questions.iloc[idxs]
considered_questions.to_csv("TrainQuestions.csv")
print(len(considered_questions))
considered_answers = answers[answers['ParentId'].isin(considered_questions['Id'])]
print(len(considered_answers))
considered_answers.to_csv("TrainAnswers.csv")
considered_tags = tags[tags['Id'].isin(considered_questions['Id'])]
print(len(considered_tags))
considered_tags.to_csv("TrainTags.csv")


# In[ ]:



