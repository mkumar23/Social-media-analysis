'''
Created on Mar 2, 2015

@author: Mrinal
'''
from os import listdir
from os.path import join as joinpath
from collections import defaultdict
from gensim import corpora, models, similarities
from nltk.tokenize import word_tokenize
import numpy as np
from gensim.models import hdpmodel, ldamodel
from itertools import izip
from nltk.corpus import stopwords
import nltk
from dateutil import parser
import datetime
import operator

window = 14
dates = []
def getDates():
    global window,dates
    preDateList = []
    postDateList = []
    avoidCeleb = []
    
    with open("celebritySuicide.csv", "r") as cs:
        for line in cs:
            dt = parser.parse(line.split('\t')[0]).date()
            dates.append(dt)
            usr = line.split('\t')[-1].strip()
            if usr not in avoidCeleb:
                for i in range(window+1):
                    postDateList.append(dt + datetime.timedelta(i))
                    if i != 0: 
                        preDateList.append(dt - datetime.timedelta(i))
    return preDateList, postDateList


def getBOW(predatelist, postdatelist):
    
    
    print len(predatelist), len(postdatelist)
    stpwrds = stopwords.words('english')
    path = './unique/posts'
    stpwrds = stopwords.words("english")
    idList = []
    doclist = [joinpath(path, fname) for fname in listdir(path) if fname.endswith('.txt')]
    
    count = 1
    predoc = []
    postdoc = []
    for file in doclist:
        with open(file,'r') as posts:
            for line in posts:
                if parser.parse(line.split('\t')[1]).date() in predatelist:
                    predoc.append(line.split('\t')[-1].decode('utf-8','ignore'))
                elif parser.parse(line.split('\t')[1]).date() in postdatelist:
                    postdoc.append(line.split('\t')[-1].decode('utf-8','ignore')) 
    
    texts1 = [[word for word in document.lower().split() if word not in stpwrds] for document in predoc]
    texts2 = [[word for word in document.lower().split() if word not in stpwrds] for document in postdoc]             
    all_tokens_pre = sum(texts1, [])
    all_tokens_post = sum(texts1, [])
    tokens_once1 = set(word for word in set(all_tokens_pre) if all_tokens_pre.count(word) == 1)
    tokens_once2 = set(word for word in set(all_tokens_post) if all_tokens_post.count(word) == 1)
    texts1 = [[word for word in text if word not in tokens_once1 and word not in stpwrds and word.isalpha()] for text in texts1]
    texts2 = [[word for word in text if word not in tokens_once2 and word not in stpwrds and word.isalpha()] for text in texts2]
    return texts1, texts2


def ExtractTopics(numTopics=5, numwrds=10):
    global window
    # filename is a pickle file where I have lists of lists containing bag of words
    predatelist, postdatelist = getDates()
    textspre, textpost = getBOW(predatelist, postdatelist)
    combined = textspre
    combined.extend(textpost)
    # generate dictionary
    dict = corpora.Dictionary(combined)
    
    # remove words with low freq.  3 is an arbitrary number I have picked here
#     low_occerance_ids = [tokenid for tokenid, docfreq in dict.dfs.iteritems() if docfreq == 3]
#     dict.filter_tokens(low_occerance_ids)
    dict.compactify()
    preCorpus = [dict.doc2bow(t) for t in combined]
    # Generate LDA Model
    lda = models.ldamodel.LdaModel(preCorpus, num_topics=numTopics)
    i = 0
    
    txt = ""
    for topic in lda.show_topics(num_topics=numTopics, num_words= numwrds, log = True, formatted=False):
        i = i + 1
        
        txt += "Topic #" + str(i) + ":\t"
        for p, id in topic:
            txt += dict[int(id)] + "\t"

        txt +='\n'
    with open('ModelledTopic'+str(window)+'days', 'w') as top:
        top.write(txt)    
    return lda, textspre, textpost, combined


lda, preCorp, postCorp, combined = ExtractTopics(50,250)

dictionary = corpora.Dictionary(combined)
# low_occerance_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 3]
# dictionary.filter_tokens(low_occerance_ids)
for dt in dates:
    predatelist = [dt - datetime.timedelta(days=x) for x in range(1, window)]
    postdatelist = [dt + datetime.timedelta(days=x) for x in range(0, window)]
    preCorp, postCorp = getBOW(predatelist, postdatelist)
    day = str(dt.month) + str(dt.day) + str(dt.year)
    with open('ldaOutput.csv','a') as out:
        topicMean = defaultdict(float)
        count = 0
        for corp in preCorp:
            count += 1
            if count == 1427:
                pass
            try:
                for (t,p) in lda[dictionary.doc2bow(corp)]:
                    topicMean[t] += p 
#                 out.write(str(lda[dictionary.doc2bow(corp)])+'\n')
            except IndexError:
                print count
        out.write('\n'+day+'\nPre-Suicide\n')
        for topic,mean in topicMean.iteritems():
            out.write(str(topic)+', '+ str(mean/count) + '\n')
    print 'Total : ',count
    
    with open('ldaOutput.csv','a') as out:
        topicMean = defaultdict(float)
        count = 0
        for corp in postCorp:
            count += 1
            if count == 717:
                pass
            try:
#                 out.write(str(lda[dictionary.doc2bow(corp)])+'\n')
                for (t,p) in lda[dictionary.doc2bow(corp)]:
                    topicMean[t] += p 
            except IndexError:
                print count
    
        out.write('\nPost Suicide\n')  
        for topic,mean in topicMean.iteritems():
            out.write(str(topic)+', '+ str(mean/count) + '\n')
    
    print 'Total : ',count