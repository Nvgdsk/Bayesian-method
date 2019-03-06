import requests
from bs4 import BeautifulSoup
from random import choice, uniform
from time import sleep
import math

arr_url=[]

url1="https://korrespondent.net/Default.aspx?page_id=60&lang=ru&stx=%D0%9D%D0%B5%D0%B4%D0%B2%D0%B8%D0%B6%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D1%8C&roi=0&st=1&p=numberpage"
url2="https://korrespondent.net/Default.aspx?page_id=60&lang=ru&isd=1&roi=0&tp=0&st=1&stx=%D1%8D%D0%BD%D0%B5%D1%80%D0%B3%D0%B5%D1%82%D0%B8%D0%BA%D0%B0&y=&p=numberpage"
url3="https://korrespondent.net/Default.aspx?page_id=60&lang=ru&isd=1&roi=0&tp=0&st=1&stx=%D0%9A%D0%B8%D0%BD%D0%BE&y=&p=numberpage"

############ parsing news
arr_url.append(url1)
arr_url.append(url2)
arr_url.append(url3)
a = []
counter = 0
for url in arr_url:
    a.append([])
    i=2
    while(i<14):
            url1  = url.replace("numberpage",str(i))
            r = requests.get(url1)
            soup = BeautifulSoup(r.text, 'html.parser')
#             f = soup.find_all("div",{"class":"textov"})
            f = soup.find_all("div",{"class":"article__title"})
            for item in f:
                
                x= item.find("a").text
                if(x!=""):
                    a[counter].append(x.lower().replace("\n","").replace("\r","").replace("  ","")) ### adding to array
            i+=1
    
    counter+=1
    
    lenarr = 0
countw = 0
limit=0
limit_to = int(limit*100/70)
if(limit_to==0 or limit_to>(min(len(a[0]),len(a[1]),len(a[2])))):
    limit_to=min(len(a[0]),len(a[1]),len(a[2]))
if(limit == 0):
    limit=min(len(a[0]),len(a[1]),len(a[2]))

lenarr+=len(a)*limit
probability = []

for row in a:
    probability.append(len(row[0:limit])/lenarr)
    
arr_text=[]
counter = 0

for row in a:
    text = ""
    arr_text.append([])
    if(limit == 0):
        limit = len(row)
    for item in row[0:limit]:
        text = text+item + " "
        
    arr_text[counter].append(text)
    
    counter+=1

def count_words(text, words):
    r = 0
  
    for w in text:
        
        
        if(w==words):
            r+=1
    return r
r=[]

count_max = 0
for row in arr_text:
    
    
    text = row[0]
    
    dict_w= dict()
    for item in text.split(" "):
        
        x = item
        
        if(x!=""):
            count_w=count_words(text.split(" "),x)
            x=item.replace('"',"",999).replace("-","",999).replace(",","",999).replace(":","",999).replace(".","",999).replace(" ","",999)
            dict_w[x]= count_w
    r.append(dict_w) 
                
                
    
    
    countw+=1
arrkey= []
for row in r:
    for key in row:
        
        arrkey.append(key)
clean_arr = []
for word in arrkey:
    if word not in clean_arr:
        clean_arr.append(word)
final_arr = []
temp = dict()

for word in clean_arr:
    text = word
    arr = []
    count_w = 0
    
    for row in r:
        if word in row:
            arr.append(row[word])
        else:
            r[r.index(row)][word]=0
            text+="\t" +str(row[word])
            arr.append(row[word])
    arr.append(sum(arr))
    temp[word] = arr
    
#     final_arr.append(temp)
    try:
        arr=[(temp[word][3]*(temp[word][0]/temp[word][3])+probability[0])/(temp[word][3]+1),(temp[word][3]*(temp[word][1]/temp[word][3])+probability[1])/(temp[word][3]+1),(temp[word][3]*(temp[word][2]/temp[word][3])+probability[2])/(temp[word][3]+1)]
        arr=[round(arr[0],2),round(arr[1],2),round(arr[2],3)]

        temp[word] = arr
    except Exception:
        temp[word] = [0,0,0]
for row in a:
    disgused= 0
    c_d=0
    if(limit_to==0 or limit_to>=len(row) ):
        limit_to=len(row)
    for title in row:
        c_d+=1
        log = []
        log.append(math.log2(probability[0]))
        log.append(math.log2(probability[1]))
        log.append(math.log2(probability[2]))
        for word in title.split(" "):
            word=word.replace('"',"",999).replace("-","",999).replace(",","",999).replace(":","",999).replace(".","",999).replace(" ","",999)
            try:
                log[0]+=math.log2(temp[word][0])
                log[1]+=math.log2(temp[word][1])
                log[2]+=math.log2(temp[word][2])
            except Exception:
                log[0] = 0
                log[1] = 0
                log[2] = 0
        if(log[0]==log[1]==log[2]):
            continue
        if(log.index(max(log))==a.index(row)):
            disgused +=1
        
#         print(title + ":" + ar_news[log.index(max(log))])
    print("It was guessed: "+str(disgused/c_d*100)+"%")
    
    


###################################################################################################
ar_news = dict()
ar_news={0:"Недвижимость",1:"Енергетика",2:"Кино"}
title = "Земельные махинации: Холодницкий сообщил о подозрении скандальному депутату Киевсовета Крымчаку "
title = title.lower()
log = []
log.append(math.log2(probability[0]))
log.append(math.log2(probability[1]))
log.append(math.log2(probability[2]))
for word in title.split(" "):
    word=word.replace('"',"",999).replace("-","",999).replace(",","",999).replace(":","",999).replace(".","",999).replace(" ","",999)
    try:
        log[0]+=math.log2(temp[word][0])
        log[1]+=math.log2(temp[word][1])
        log[2]+=math.log2(temp[word][2])
    except Exception:
        log[0] += 0
        log[1] += 0
        log[2] += 0
print(log)
print(title + ":" + ar_news[log.index(max(log))])
