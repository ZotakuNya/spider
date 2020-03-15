from myModels import *

q=Queue()
NUM=7
URLlist=[]
tmpDict={}
baseListPage='https://segmentfault.com/questions?page='

def working():
    while(True):
        listpage=q.get()
        getURLlist(listpage,tmpDict,proxies)
        print(listpage)
        time.sleep(1)
        q.task_done()

for i in range(NUM):
    t=Thread(target=working)
    t.setDaemon(True)
    t.start()

for i in range(1,5736):#5729
    listpage=baseListPage+str(i)
    q.put(listpage)

q.join()

URLlist=sorted(tmpDict.items(), key=lambda x:x[1], reverse=True)

with open('url.txt','w',encoding='utf-8') as f2:
    for item in URLlist:
        f2.write(item[0]+'\n')
    f2.close()

