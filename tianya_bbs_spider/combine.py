import glob
import csv

csvx_list = glob.glob('*.csv')
tmp=[]

for i in csvx_list:
    fl=open(i,'r',encoding='utf-8')
    reader=csv.reader(fl)
    for item in list(reader):
        tmp.append(item)

ls=[]
for item in tmp:
    if (item not in ls):
        ls.append(item)

with open('result.csv','w',encoding='utf-8') as fl:
    writer=csv.writer(fl)
    for row in ls:
        writer.writerow(row)
