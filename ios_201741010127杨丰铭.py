import requests
from bs4 import BeautifulSoup
import multiprocessing as mp 
import time

t1 = time.time()
r = requests.get('http://www.ireader.com/index.php?ca=booksort.index&pid=92&cid=93&order=download&status=0&page=1')

c = r.text
soup = BeautifulSoup(c,'html.parser')
page_div = soup.find('div',{'class':'changepage'})
page = page_div.find_all('a')[-2].text
notes = []

urls = ['http://www.ireader.com/index.php?ca=booksort.index&pid=92&cid=93&order=download&status=0&page=' + str(i) for i in range(1,11)]

def crawl_page(url):
    p_r = requests.get(url)
    p_c = p_r.text
    p_soup =BeautifulSoup(p_c,'html.parser')
    p_content=p_soup.find('div',{'class':'changepage'})
    pageNote = []
    for note in p_content:
        noteDic = {}
        noteDic['name'] = note.find('div',{'class':'bookMation'}).find('a').text
        noteDic['int'] = note.find('p',{'class':'introduce'}).text
        pageNote.append(noteDic)
    return pageNote

pool = mp.Pool()
multi_res = [pool.apply_async(crawl_page,(url,)) for url in urls]
pageNotes = [res.get() for res in multi_res]
for pageNote in pageNotes:
    for note in pageNote:
        notes.append(note)
print(len(notes))
t2 = time.time()
print(t2-t1)
