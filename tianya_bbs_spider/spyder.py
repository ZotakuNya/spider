import bs4
import requests
import re
import time
import csv
import io
import sys

def get_html(url):
    try:
        res=requests.get(url)
        assert res.status_code==200
        return res.text
    except:
        print(url)

def get_content(url):
    html=get_html(url)
    soup=bs4.BeautifulSoup(html,'html.parser')
    row_content=soup.findAll(name='div',attrs={'class':"bbs-content clearfix"})
    content=row_content[0].text.strip().replace(u'\u3000', u'')
    row_comment=soup.findAll(name='div',attrs={'class':'atl-item'})
    del row_comment[0]
    comment_list=[]
    if len(row_comment) is not 0:
        for comment in row_comment:
            main_author=re.findall(r'_host=".*?"',str(comment))[0].split('"')[1]
            main_comment=comment.findAll(name='div',attrs={'class':'bbs-content'})[0].text.strip()
            comment_list.append({main_author:main_comment})
            re_cmt_ls=comment.findAll(name='li')
            if len(re_cmt_ls) is not 0:
                for re_cmt in comment.findAll(name='li'):
                    re_cmt_author=re.findall(r'_username=".*?"',str(re_cmt))[0].split('"')[1]
                    re_cmt_content=re.sub(r'<.*?>','',re.findall(r'评论.*</span>',str(re_cmt),re.S)[0])
                    comment_list.append({re_cmt_author:re_cmt_content})
    return content,comment_list

def get_posts(url,tag,index,start_index):
    html=get_html(url)
    soup=bs4.BeautifulSoup(html,'html.parser')
    ls=soup.findAll(name='tr')
    del ls[0]
    posts_list=[]
    for post in ls:
        if ('<span class="art-ico art-ico-9"></span>' in str(post)) == 0:
            title=post.findAll(name='a')[0].text.strip()
            author=post.findAll(name='a')[1].text.strip()
            #time=re.findall(r'\d\d\d\d-\d\d-\d\d',str(post))[0]
            if(not 'http://bbs.tianya.cn' in re.findall(r'href=".*?html"',str(post))[0].split('"')[1]):
                post_url='http://bbs.tianya.cn'+re.findall(r'href=".*?html"',str(post))[0].split('"')[1]
            else:
                post_url=re.findall(r'href=".*?html"',str(post))[0].split('"')[1]
            content,comment_list=get_content(post_url)
            posts_list.append([tag,title,content,comment_list])
        else:
            continue
    with open(tag+str(index+start_index)+'.csv', 'w', newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        for row in posts_list:
            writer.writerow(row)

url=input("输入起始页链接:")
tag=input('输入TAG:')
pages=int(input('输入要爬的页数:'))
start_index=int(input('输入起始序号:'))

for i in range(pages):
    get_posts(url,tag,i,start_index)
    url='http://bbs.tianya.cn'+re.findall(r'/list.*?" rel="nofollow">下一页</a>',get_html(url))[0].split('"')[0]



