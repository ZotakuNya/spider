import pymongo
import collections
import k_means

col=pymongo.MongoClient().userData.users

'''
for dic in col.find():
    m=0
    for key in dic:
        if(isinstance(dic[key],int)):
            m=m+dic[key]
    if(m==0):
        for key in dic:
            if(isinstance(dic[key],int)):
                dic[key]=1
    col.update({'_id':dic['_id']},dic)    
'''

for dic in col.find():
    m=0
    for key in dic:
        if(isinstance(dic[key],int)):
            m=m+dic[key]
    if(m==0):
        col.delete_one({'_id':dic['_id']})

ls=list(col.find())

for dic in ls:
    m=0
    for key in dic:
        if(isinstance(dic[key],int)):
            m=m+dic[key]
    del dic['_id']
    for key in dic:
        if(isinstance(dic[key],int)):
            dic[key]=round((float(dic[key])/float(m))*100,2)

wd=[]
for dic in ls:
        for key in dic:
            wd.append(key)

count=collections.Counter(wd)

wd=[]
ct=0

for x in count:
    if(x!='id'):
        wd.append(x)
        #print(x+':'+str(count[x]))
    ct+=1
    if(ct==101):
        break

#print(wd)

userdata={}
dataSet=[]

#print(wd)

for dic in ls:
    tmp=[]
    for tag in wd:
        tmp.append(tag)
    for i in range(100):
        for key in dic:
            if(key==tmp[i]):
                tmp[i]=dic[key]
    for i in range(100):
        if(isinstance(tmp[i],str)):
            tmp[i]=0
    dataSet.append(tmp)
    userdata[dic['id']]=tmp

'''
for x in range(10):
    print(dataSet[x])
'''

for x in reversed(range(len(dataSet))):
    #print(dataSet[x])
    if(not sum(dataSet[x])):
        del dataSet[x]

centroids=[]
for x in range(20):
    centroids.append(dataSet[x])

dataSet=k_means.mat(dataSet)
centroids=k_means.kMeans(dataSet,20,k_means.mat(centroids))


fl=[]
for x in range(20):
    fl.append(open('sort2/'+str(x)+'.txt','w',encoding='utf-8'))

for x in userdata:
    num=0
    distance=k_means.distEclud(centroids[0],userdata[x])
    for i in range(1,20):
        if(k_means.distEclud(centroids[i],userdata[x])<distance):
            distance=k_means.distEclud(centroids[i],userdata[x])
            num=i
    fl[num].write(x+'\n')

for x in range(20):
    fl[x].close()
