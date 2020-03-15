import k_means
import pymongo

col=pymongo.MongoClient().userData.users

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
            dic[key]=round((float(dic[key])/float(m))*100,0)

dataSet=[]
userdata={}

wd=[
    ['javascript','html','css','react_js','jquery','node_js'],
    ['c','c++','mfc'],
    'php',
    ['java','android','jdk8','java-ee'],
    ['python','python3_x','python2_7','pywin32'],
    ['ios','objective-c'],
    ['swift','ios7'],
    ['c#','unity','unity2d'],
    'golang'
    ]

for dic in ls:
    tmp=[]
    for tag in wd:
        tmp.append(tag)
    for i in range(len(wd)):
        if(not isinstance(tmp[i],list)):
            for key in dic:
                if(key==tmp[i]):
                    tmp[i]=dic[key]
        else:
            n=0.0
            for x in range(len(tmp[i])):
                for key in dic:
                    if(key==tmp[i][x]):
                        n+=dic[key]
            tmp[i]=n
    for i in range(len(wd)):
        if(isinstance(tmp[i],str) or isinstance(tmp[i],list)):
            tmp[i]=0
    dataSet.append(tmp)
    userdata[dic['id']]=tmp

for x in reversed(range(len(dataSet))):
    #print(dataSet[x])
    if(not sum(dataSet[x])):
        del dataSet[x]

t=list(userdata.keys())
for x in t:
    if (not sum(userdata[x])):
        del userdata[x]

centroids=[]
for x in range(9):
    centroids.append(dataSet[x])

print(len(dataSet))

dataSet=k_means.mat(dataSet)
centroids=k_means.kMeans(dataSet,9,k_means.mat(centroids))

fl=[]
for x in range(9):
    fl.append(open('sort/'+str(x)+'.txt','w',encoding='utf-8'))

for x in userdata:
    num=0
    distance=k_means.distEclud(centroids[0],userdata[x])
    for i in range(1,9):
        if(k_means.distEclud(centroids[i],userdata[x])<distance):
            distance=k_means.distEclud(centroids[i],userdata[x])
            num=i
    fl[num].write(x+'\n')

for x in range(9):
    fl[x].close()
    
