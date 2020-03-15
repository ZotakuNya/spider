from myModels import *

q=Queue(10) #创建队列
NUM=3
f1=open('userUrl8.txt','w',encoding='utf-8')
f2=open('tag8.txt','w',encoding='utf-8')

def working():
    while(True):
        url=q.get() #从队列取值
        html=getHTML(url)
        for txt in getTag(html):
            f2.write(txt)
        for txt in getUserUrl(html):
            f1.write(txt)
        time.sleep(0.5)
        q.task_done()
        if(q.empty()):
            break

for i in range(NUM): #创建线程
    t=Thread(target=working)
    t.setDaemon(True)
    t.start()

with open('./url/url8.txt','r',encoding='utf-8') as fl:
    for url in fl:
        if(url):
            q.put(url[:-1])
    q.join()
    fl.close()

f1.close()
f2.close()
