from myModels import *

q=Queue(10)
NUM=3

col=pymongo.MongoClient().userData.data

def working():
    while(True):
        url=q.get()
        col.insert(getUserData(url))
        time.sleep(0.5)
        q.task_done()
        if(q.empty()):
            break


for i in range(NUM):
    t=Thread(target=working)
    t.setDaemon(True)
    t.start()

with open('userUrl.txt','r',encoding='utf-8') as fl:
    ls=list(set(list(fl)))
    for url in ls:
        if(url):
            q.put(url[:-1])
            #col.insert(getUserData(url[:-1]))
            #time.sleep(0.5)
    q.join()
    fl.close()
