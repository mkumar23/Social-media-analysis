'''
Created on Jan 25, 2015

@author: Mrinal
'''
from os import listdir
from os.path import join as joinpath
from _collections import defaultdict

path = './posts'
count = defaultdict(int)
idList = []
trollUserList =[]
doclist = [joinpath(path, fname) for fname in listdir(path) if fname.endswith('.txt')]
with open('./users/trollusers.txt','r') as fake:
    for line in fake:
        trollUserList.append(line.strip(' ').split('/')[-1].rstrip('\n').strip(' '))
         

print trollUserList
filter =0
total = 0
for file in doclist:
    with open(file,'r') as posts:
        for line in posts:
            id, a, user= line.split('\t')[0], line.split('\t')[1], line.split('\t')[2]
            if id not in idList and user not in trollUserList:
                idList.append(id)
                count[a.split(' ')[0]] += 1
                filter += 1
            total += 1
            
print filter,total
with open('postCount.txt','w') as outp:
    for a,b in count.iteritems():
        outp.write(a+'\t'+str(b)+'\n')