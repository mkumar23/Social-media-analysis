'''
Created on Feb 3, 2015

@author: Mrinal
'''
from os import listdir
from os.path import join as joinpath
from _collections import defaultdict
from nltk.corpus import stopwords
import nltk
from dateutil import parser
import datetime
import operator

stpwrds = stopwords.words("english")
window = 14
path = './unique/posts'
count = defaultdict(int)
idList = []
txt = ""
datelist = []
predate = []
postdate = []
total = 0
inRange = 0
with open("celebritySuicide.csv", "r") as cs:
    for line in cs:
        dt = parser.parse(line.split('\t')[0]).date()
        for i in range(window+1):
            datelist.append(dt + datetime.timedelta(i))
            postdate.append(dt + datetime.timedelta(i))
            if i != 0: 
                datelist.append(dt - datetime.timedelta(i))
                predate.append(dt - datetime.timedelta(i))
            
prepost = []
post_post = []
doclist = [joinpath(path, fname) for fname in listdir(path) if fname.endswith('.txt')]
for file in doclist:
    with open(file,'r') as posts:
        for line in posts:
            dt = parser.parse(line.split('\t')[1]).date()
            if(dt in datelist):
                txt += line.split('\t')[-1]
                inRange += 1
            if dt in predate:
                prepost += line.split('\t')[-1]
            elif dt in postdate:
                post_post += line.split('\t')[-1]
            total += 1


print total, inRange
tokens = nltk.word_tokenize(txt.decode('ascii','ignore'))
fdistUni = nltk.FreqDist(tokens)
bgms = nltk.bigrams(tokens) 
fdistBi = nltk.FreqDist(bgms)
tgms = nltk.trigrams(tokens)
fdistTri = nltk.FreqDist(tgms)

with open("unigramFrequency"+str(window)+"win.freq","w") as uf:
    for w,f in sorted(fdistUni.items(), key = operator.itemgetter(1), reverse = True):
        if f > 100 and (w.encode('ascii') not in stpwrds and w[0].encode('ascii').isalnum()): 
            uf.write(w.encode('ascii')+'\t'+str(f)+'\n')

with open("bigramFrequency"+str(window)+"win.freq","w") as bf:
    for w,f in sorted(fdistBi.items(), key = operator.itemgetter(1), reverse = True):
        if f > 100 and ((w[0].encode('ascii') not in stpwrds and w[0].encode('ascii').isalnum()) or (w[1].encode('ascii') not in stpwrds and w[0].encode('ascii').isalnum())): 
            bf.write(w[0].encode('ascii')+'\t'+w[1].encode('ascii')+'\t'+str(f)+'\n')

with open("trigramFrequency"+str(window)+"win.freq","w") as tf:
    for w,f in sorted(fdistTri.items(), key = operator.itemgetter(1), reverse = True):
        if f > 50 and ((w[0].encode('ascii') not in stpwrds and w[0].encode('ascii').isalnum()) or (w[1].encode('ascii') not in stpwrds and w[0].encode('ascii').isalnum())): 
            tf.write(w[0].encode('ascii')+'\t'+w[1].encode('ascii')+'\t'+w[2].encode('ascii')+'\t'+str(f)+'\n')
