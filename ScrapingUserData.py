import pandas as pd
from urllib.request import urlopen
import json
import io
import gzip
import math
import numpy as np
import stackexchange
import time
import copy

so = stackexchange.Site(stackexchange.StackOverflow, 'NWEfvT9FqBahe5FKdZg0Wg((')

dataset = []
dataset.append(['Row','Bronze Badges','Silver Badges','Gold Badges','Account Id','Is Employee',\
'Reputation','User Id','Accept Rate'])
def parseData(fname):
    response = urlopen(fname)
    buf = io.BytesIO(response.read())
    gzip_f = gzip.GzipFile(fileobj=buf)
    content = gzip_f.read().decode("utf-8")
    obj = json.loads(content)
    return obj
badurls = []
missingdata = 0
print("Reading data")
questions = pd.read_csv("input/TrainQuestions.csv", encoding='latin1')
userids = questions['OwnerUserId'].unique()
print("Done")
counter = 0
requests = 0
badurlstart = 0
for i in range(0,len(userids),25):#len(userids),30):
    if not i % 1000:
        print(i)
    useridstoconsider = userids[i:i+25]
    ids = ';'.join([str(int(x)) for x in useridstoconsider if not math.isnan(x)])
    urlstr = "https://api.stackexchange.com/2.2/users/" + ids + "?key=NWEfvT9FqBahe5FKdZg0Wg((&order=desc&sort=reputation&site=stackoverflow"
    #print (urlstr)
    requests += 1
    if requests % 30 == 0:
        print("Sleeping...")
        time.sleep(5)
        print("Continuing")
    try:
        data = parseData(urlstr)
    except Exception as e:
        print(i, e, urlstr)
        badurls.append((urlstr,i))
        if badurlstart == 0:
            badurlstart = i
    if len(data['items']) != 25:
        print ("Not 25 but ",len(data['items']))
        missingdata += (25 - len(data['items']))
    for item in data['items']:
        datarow = [str(counter),item['badge_counts']['bronze'],item['badge_counts']['silver'], \
        item['badge_counts']['gold'], item['account_id'], item['is_employee'],\
        item['reputation'],item['user_id'],item['accept_rate'] if\
         'accept_rate' in item else 'NA']
        dataset.append(copy.deepcopy(datarow))
        counter += 1
dataset = np.array(dataset)

df = pd.DataFrame(data=dataset[1:,1:],
                  index=dataset[1:,0],
                  columns=dataset[0,1:])
df.to_csv('users_new.csv')

print("Bad URLS:",badurls)
print("Missing Data:", missingdata)
print("Index of Bad URL Start:",i)
