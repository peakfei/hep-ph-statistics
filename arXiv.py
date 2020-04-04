#!/Users/peakfei/anaconda3/bin/python
import requests
from lxml import etree
import numpy as np
import matplotlib.pyplot as plt

def string_year(year=2020):
    '''change year to the standard form used by arXiv, i.e, the last number of year'''
    a = str(year%100)
    if len(a)==1:
        a='0'+a
    return a
def string_month(month=1):
    '''change month to the standard form used by arXiv, 1-9 to 01-09'''
    a = str(month)
    if len(a)==1:
        a='0'+a
    return a
def num_papers(year=2019):
    '''return a list about the number of papers per month'''
    s_year=string_year(year)
    n_month=0
    if s_year=='20':
        n_month=3
    elif s_year=='92':
        n_month=10
    else:
        n_month=12
    url = 'https://arxiv.org/year/hep-ph/'+s_year
    r=requests.get(url).text
    s = etree.HTML(bytes(r, encoding='utf-8'))
    npapers=[]
    for i in range(n_month):
        ph = s.xpath('//*[@id="content"]/ul/li[' + str(i+1) + ']/b/text()')
        cross = s.xpath('//*[@id="content"]/ul/li[' + str(i+1) + ']/i/text()')
        npapers.append(int(ph[0])+int(cross[0]))
    return npapers

def download_paper_names(year=1999,month=1):
    '''download the name of papers and store in files'''
    s_year=string_year(year)
    s_month=string_month(month)

    n_papers = num_papers(year)
    if year==1992:
        i=n_papers[month-3]
    else:
        i=n_papers[month-1]
    ar_title = []
    url='https://arxiv.org/list/hep-ph/'+s_year + s_month+'?show='+str(i)
    r=requests.get(url).text
    s = etree.HTML(bytes(r, encoding='utf-8'))
    for index in range(i):
        raw = s.xpath('//*[@id="dlpage"]/dl/dd[' + str(index+1) + ']/div/div[1]/text()')[1]
        ar_title.append(raw[:-1])
        #print(index+1,raw[:-1])

    # write to file
    with open('arXiv_data/data_'+s_year+s_month+'.txt', 'w') as f:
        for item in ar_title:
            #print(item)
            f.write('%s\n'%item)
    #return ar_title
def read_list_papers_month(year=1993,month=1):
    ''' read the names of paper from files at certain year and month'''
    s_year=string_year(year)
    s_month=string_month(month)
    with open('arXiv_data/data_'+s_year+s_month+'.txt', 'r') as f:
        while True:
            item = f.readline()
            if not item:
                break
            print(item.strip().lower())
def read_list_papers(year=1993):
    ''' read the names of paper from files at certain year'''
    s_year=string_year(year)
    list_papers=[]
    if year==1992:
        range_month=range(3,13)
    elif year==2020:
        range_month=range(1,4)
    else:
        range_month=range(1,13)

    for month in range_month:
        s_month=string_month(month)
        with open('arXiv_data/data_'+s_year+s_month+'.txt', 'r') as f:
            while True:
                item = f.readline()
                if not item:
                    break
                list_papers.append(item.strip().lower())
    return list_papers
def asked_number_of_papers(keys=['dark matter'],year=1995):
    '''return the number of paper satisfing keywords'''
    aaa=read_list_papers(year)
    ar_res=[]
    for title in aaa:
        res=[]
        for key in keys:
            if key in title:
                res.append(1)
            else:
                res.append(0)
        ar_res.append(res)
    return np.sum(np.array(ar_res),axis=0)

##example : download,
##the papers' name for 1992-2019 has already been downloaded and stored in arXiv_data
#for month in range(3,4):
#    download_paper_names(year=2020,month=month)

##example : inquire for the number of paper from 1992 to 2020
##it while take a while, about 1min
#x = list(range(1992,2021))
#y = [np.sum(num_papers(i)) for i in x]
##show
#plt.plot(x[:-1],y[:-1],'b-')
#plt.xlabel('year')
#plt.ylabel('number of paper')
#plt.show()

## example: list number of paper with keyword
keys=['dark matter','higgs','neutrino','inflation','gravitational','black hole']
years=range(1992,2020)
ar = []
for year in years:
    temp = asked_number_of_papers(keys,year)
    print(year, ":", temp)
    ar.append(list(temp))

## show
for i in range(len(keys)):
    plt.plot(list(years),np.array(ar)[:,i],label=keys[i])
plt.legend()
plt.xlabel('Year')
plt.ylabel('num of paper')
plt.show()

