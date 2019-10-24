import requests #pip3 install requests
from bs4 import BeautifulSoup #pip3 install bs4
import multiprocessing as mp
import time

t1=time.time()
r=requests.get('https://xiaoshuo.sogou.com/36_0_0_0_heat/?pageNo=1')
c=r.text
soup=BeautifulSoup(c,'html.parser')
#content=soup.find_all('ul',{'class':'filter-ret clear'})
page_div=soup.find('div',{'class':'pages'})
page=page_div.find_all('a')[-2].text
books=[]
urls=['https://xiaoshuo.sogou.com/36_0_0_0_heat/?pageNo='+str(i) for i in range(1,285)]
def crawl_page(url):
    p_r=requests.get(url)
    p_c=p_r.text
    p_soup=BeautifulSoup(p_c,'html.parser')
    p_f=p_soup.find('ul',{'class':'filter-ret clear'})
    p_content=p_f.find_all('li',{'class':'fl clear'})
    pageBook=[]
    for book in p_content:
        bookDic={}   
        bookDic['picUrl']=book.find('a',{'class':'cover fl'}).find('img')['src']
        #print(bookDic['picUrl'])
        bookDic['name']=book.find('div',{'class':'info fl'}).find('h3').find('a').text
#print(name)
        bookDic['sub']=book.find('div',{'class':'d2'}).text
#print(sub)
        pageBook.append(bookDic)
    return pageBook
pool=mp.Pool()
multi_res=[pool.apply_async(crawl_page,(url,)) for url in urls]
pageBooks=[res.get() for res in multi_res]

for pageBook in pageBooks:
    for book in pageBook:
        books.append(book)
print(books[-1])
t2=time.time()
print(t2-t1)
