'''
Created on Feb 9, 2015

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
def getDates():
    global window
    preDateList = []
    postDateList = []
    with open("celebritySuicide.csv", "r") as cs:
        for line in cs:
            dt = parser.parse(line.split('\t')[0]).date()
            for i in range(window+1):
                postDateList.append(dt + datetime.timedelta(i))
                if i != 0: 
                    preDateList.append(dt - datetime.timedelta(i))
    return preDateList, postDateList

def getBOW():
    
    predatelist, postdatelist = getDates()
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
    textspre, textpost = getBOW()

    # generate dictionary
    dict = corpora.Dictionary(textspre)

    # remove words with low freq.  3 is an arbitrary number I have picked here
    low_occerance_ids = [tokenid for tokenid, docfreq in dict.dfs.iteritems() if docfreq == 3]
    dict.filter_tokens(low_occerance_ids)
    dict.compactify()
    corpus = [dict.doc2bow(t) for t in textspre]
    # Generate LDA Model
    lda = models.ldamodel.LdaModel(corpus, num_topics=numTopics)
    i = 0
    # We print the topics
    txt = ""
    for topic in lda.show_topics(num_topics=numTopics, num_words= numwrds, log = False, formatted=False):
        i = i + 1
        
        txt += "Topic #" + str(i) + ":\t"
        for p, id in topic:
            txt += dict[int(id)] + "\t"

        txt +='\n'
    with open('PreModelledTopic'+str(window)+'days', 'w') as top:
        top.write(txt)    
        
    dict = corpora.Dictionary(textpost)

    # remove words with low freq.  3 is an arbitrary number I have picked here
    low_occerance_ids = [tokenid for tokenid, docfreq in dict.dfs.iteritems() if docfreq == 3]
    dict.filter_tokens(low_occerance_ids)
    dict.compactify()
    corpus = [dict.doc2bow(t) for t in textpost]
    # Generate LDA Model
    lda = models.ldamodel.LdaModel(corpus, num_topics=numTopics)
    i = 0
    # We print the topics
    txt = ""
    for topic in lda.show_topics(num_topics=numTopics, num_words= numwrds, log = False, formatted=False):
        i = i + 1
        
        txt += "Topic #" + str(i) + ":\t"
        for p, id in topic:
            txt += dict[int(id)] + "\t"

        txt +='\n'
    with open('PostModelledTopic'+str(window)+'days', 'w') as top:
        top.write(txt)    


ExtractTopics(10,20)      


