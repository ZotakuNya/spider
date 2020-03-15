import re
import requests
import collections
import bs4
import time
from threading import Thread
from queue import Queue
import pymongo

headers={
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
}
proxies={	
    "http":"http://125.109.197.34:808",
    "http":"http://112.114.99.112:8118",
    "http":"http://112.114.97.102:8118",
    "http":"http://110.166.254.120:808",
    "http":"http://112.114.96.239:8118",
    "http":"http://106.81.230.168:8118",
    "http":"http://219.149.46.151:3129",
    "http":"http://119.29.18.239:8888",
    "http":"http://61.135.217.7:80",
    "http":"http://118.114.77.47:8080"
        }

def getHTML(url,headers=headers):
    try:
        print(url)
        r=requests.get(url,headers=headers)
        r.raise_for_status
        if(not re.findall('暂时无法对非人类提供服务, 请输入以下验证码核实身份',r.text)):
            return r.text
        else:
            input()
            r=requests.get(url,headers=headers)
            r.raise_for_status
            return r.text
    except:
        print('error1\n')

def getTag(html):
    ls=[]
    match=re.findall(r'data-original-title=".*"',html)
    if(len(match)!=1):
        for i in range(len(match)-1):
            ls.append(match[i].split('"')[1]+' ')
    return ls

def getURLlist(listpage,tmpDict,proxies=proxies):
    try:
        a=requests.get(listpage,proxies=proxies)
        a.raise_for_status
        if(not re.findall('暂时无法对非人类提供服务, 请输入以下验证码核实身份',r.text)):
            soup=bs4.BeautifulSoup(a.text,"html.parser")
            ls=soup.findAll('section',class_="stream-list__item")
            for sec in ls:
                tmp1=re.findall(r'<h2 class="title"><a href="/q/10100000.*"',str(sec))
                tmp2=re.findall(r'<span>.*</span>',str(sec))
                tmp3=str(tmp2[0])[6:-7]
                if(tmp3[-1]=='k'):
                    tmp3=float(tmp3[:-1])*1000
                tmpDict['https://segmentfault.com'+tmp1[0].split('"')[3]]=int(tmp3)
        else:
            input()
            getURLlist(listpage,tmpDict,proxies)
    except:
        print('error2\n')
'''
def getFAQ(html,FAQlist):
    soup=bs4.BeautifulSoup(html,"html.parser")
    dr = re.compile(r'<[^>]+>',re.S)
    FAQ=['question:']
    FAQ.append(dr.sub('',str(soup.find(class_="question fmt"))))
    FAQ.append('answer:')
    tmpA=soup.findAll(class_="answer fmt")
    for tag in tmpA:
        FAQ.append(dr.sub('',str(tag)))
    FAQlist.append(FAQ)
'''
def getUserUrl(html):
    ls=[]
    soup=bs4.BeautifulSoup(html,"html.parser")
    if(re.findall(r'/u/.*"',str(soup.find(class_="question__author")))):
        ls.append('https://segmentfault.com'+re.findall(r'/u/.*"',str(soup.find(class_="question__author")))[0][:-1]+'\n')
    if(soup.findAll(class_="answer__info--author-name")):
        for txt in soup.findAll(class_="answer__info--author-name"):
            if(re.findall(r'/u/.*?"',str(txt))):
                ls.append('https://segmentfault.com'+re.findall(r'/u/.*?"',str(txt))[0][:-1]+'\n')
    return ls

def getUserData(url,headers=headers):
    try:
        print(url)
        r=requests.get(url,headers=headers)
        r.raise_for_status
        if(not re.findall('暂时无法对非人类提供服务, 请输入以下验证码核实身份',r.text)):
            ls=re.findall(r'"name":".*?","incr":"\d*?"',r.text)
            for i in range(len(ls)):
                ls[i]=eval("'{}'".format(ls[i]))
            lsd={}
            lsd['id']=url[27:]
            for i in range(len(ls)):
                tx=re.sub(r'\.','_',ls[i].split('"')[3])
                lsd[tx]=int(ls[i].split('"')[-2])
            return lsd
        else:
            input()
            ls=re.findall(r'"name":".*?","incr":"\d*?"',r.text)
            for i in range(len(ls)):
                ls[i]=eval("'{}'".format(ls[i]))
            lsd={}
            lsd['id']=url[27:]
            for i in range(len(ls)):
                tx=re.sub(r'\.','_',ls[i].split('"')[3])
                lsd[tx]=int(ls[i].split('"')[-2])
            return lsd
    except:
        print('error3\n')
