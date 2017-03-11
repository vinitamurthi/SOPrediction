
# coding: utf-8

# In[283]:

import pandas as pd
import os
import copy
from sklearn.cluster import KMeans


# In[ ]:




# In[2]:

filepath = os.getcwd() + '/assignment2/input/TrainTags.csv'
data = pd.read_csv(filepath, encoding='latin1')


# In[285]:

tagCountSeries = data['Tag'].value_counts()
commonTags = tagCountSeries[:100]
commonTagsSeries = pd.Series(commonTags.index)
commonTags_df = pd.DataFrame({'QnCount':commonTags.values, 'Tag':commonTags.index})


# In[190]:

commonTagTotalQnCount = commonTags_df['QnCount'].sum()
def getPopularity(qnCount):
    return qnCount/commonTagTotalQnCount
commonTags_df['Popularity'] = commonTags_df['QnCount'].apply(getPopularity)


# In[200]:

# example of looking at one tag row
commonTags_df[commonTags_df['Tag'] == 'sql-server']


# In[211]:

# example of looking at tag's popularity
commonTags_df[commonTags_df['Tag'] == 'sql-server']['Popularity']


# In[288]:

commonTags_df[:10]


# In[ ]:

# Getting a list of all unique tags in data set
tags = data['Tag'].unique().tolist()
print(tags[:10])
print(tags.index('getter'))


# In[40]:

qnids = data['Id'].unique()


# In[41]:

# method to one hot encode all tags
def one_hot_encode_tags(tags_list):
    #create an array of 0s for all tags, + 1 for unknown tags
    encoded_tag = [0] * (len(tags) + 1)
    for tag in tags_list:
        index = tags.index(tag) if tag in tags else -1
        encoded_tag[index] = 1
    return encoded_tag


# In[192]:

# method to one hot encode most common tags (currently top 100)
def oneHotEncode_common_tags(tags_list):
    return commonTagsSeries.isin(tags_list).apply(int).tolist()


# In[ ]:

tags_by_qn = data.groupby('Id')['Tag'].apply(list)
tags_by_qn_df = pd.DataFrame({'qnid':tags_by_qn.index, 'tags':tags_by_qn.values})


# In[289]:

tags_by_qn_df[:10]


# In[206]:

# One hot encode all tags
# Notes : Takes too long
tags_by_qn_df['encoded_tags'] = tags_by_qn_df['tags'].apply(oneHotEncode_common_tags)


# In[261]:

def getQnPopularityScore(tag_list):
    avg_popularity = 0
    max_popularity = 0
    tags_popularity = commonTags_df[commonTags_df['Tag'].isin(tag_list)]['Popularity']
    if len(tags_popularity) > 0:
        avg_popularity = sum(tags_popularity)/len(tag_list)
        max_popularity = max(tags_popularity)
    return avg_popularity,max_popularity


# In[ ]:

# Get Popularity score of all Qns based on rating of common tags
tags_by_qn_df['avg_popularity'],tags_by_qn_df['max_popularity'] =     zip(*tags_by_qn_df['tags'].map(getQnPopularityScore))


# In[ ]:




# In[290]:

tags_by_qn_df[:10]


# In[282]:

# export data
tags_by_qn_df.to_csv('tags_features.csv')


# In[ ]:

X = tags_by_qn_df['encoded_tags']
kmeans = KMeans(n_clusters=100, random_state=0).fit(X.tolist())


# In[113]:

tags_by_qn_df_small = copy.deepcopy(tags_by_qn_df[:10])
tags_by_qn_df_small['encoded_tags'] = tags_by_qn_df_small['tags'].apply(one_hot_encode_tags)


# In[ ]:

# X = []
# for qnid, tag_list in tags_by_qn.iteritems():
#     feature_row = one_hot_encode_tags(tag_list)
#     feature_row.insert(0,qnid)
#     X.append(feature_row)


# In[ ]:

def tags_for_qn(qnid):
    qn_tags = data[data['Id'] == qnid]
    qn_tags_list = []
    for t in qn_tags.itertuples():
        qn_tags_list.append(t[3])

    return qn_tags_list

qnids = data['Id'].unique()
print(len(qnids))


# In[ ]:

# Each row is [qnid ,  1-hot-encoding of qns tags]
X = [[qn, one_hot_encode_tags(tags_for_qn(qn))] for qn in qnids[:10000]]


# In[6]:

data

