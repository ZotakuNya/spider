---
title: 爬虫学习笔记—requests库
date: 2017-12-12 21:52:58
tags: 
---

# 爬虫学习笔记—requests库

requests库是提供操作网页的方法的第三方库，以requests方法为核心，提供6种与HTTP协议对应的方法

HTTP协议的6种方法：

- `get`:客户端向服务端发起请求，获得资源。请求获得URL处所在的资源
- `post`:向服务端提交新的请求字段。请求URL的资源后添加新的数据
- `head`:请求获取URL资源的响应报告，即获得URL资源的头部
- `patch`：请求局部修改URL所在资源的数据项
- `put`：请求修改URL所在资源的数据元素
- `delete`：请求删除url资源的数据

> patch与put 比较：
>
> 例如一名学生的信息：姓名：张三；性别：男；学号：123；
>
> patch提交修改性别。修改后：姓名：张三；性别：女；学号：123；
>
> put提交修改性别,修改后：姓名：；性别：女；学号：；  这是因为patch是局部的，put必须提交全部数据项，即整个数据元素。增加了带宽

与之对应，requests库提供requests.get、requests.post、requests.head、requests.patch、requests.put、requests.delete这6种方法

*为什么说requests方法是基础：*

​	我们找到各方法的定义：

```python
def requests(method,url,**kwargs)           #kwargs为可选位置参数
{
  	···
}
def get(url,**kwargs):
    return requests(get,url,**kwargs)
def post(url,**kwargs):
    return requests(post,url,**kwargs)
```

​	可以看出，其他方法是对requests方法的封装，以方便开发者调用。

#### 相关参数

`params`:字典或字节序列，作为参数添加到URL中
`data`:若data=字典，则以form(表单)为Requests内容提交；若data="字符串"，则Requests data="字符串"
`json`：以json格式数据作为Requests内容
`headers`:字典，模仿浏览器行为，为Requests定制表头
`cookies`:字典或CookieJar,作为Requests的cookie
`proxies`:字典，作为代理IP,设定代理服务器
`timeout`:设定超时时间，以秒为单位
`file`:字典，传输文件
`auth`:元组，支持HTTP的认证
`stream`:True/False,默认为True，获取内容立即下载
`verify`:True/False 默认为True，认证SSL证书开关
`allow_redirects`:True/False ,默认为True.支持重定向
`cert`:本地ssl路径