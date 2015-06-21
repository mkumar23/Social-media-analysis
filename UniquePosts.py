'''
Created on Feb 3, 2015

@author: Mrinal
'''
from os import listdir
from os.path import join as joinpath
from _collections import defaultdict

path = './posts'
count = defaultdict(int)
idList = []
total = 0
unq = 0
trollUserList =[]
with open('./users/trollusers.txt','r') as fake:
    for line in fake:
        trollUserList.append(line.strip(' ').split('/')[-1].rstrip('\n').strip(' '))

doclist = [joinpath(path, fname) for fname in listdir(path) if fname.endswith('.txt')]
for file in doclist:
    with open(file,'r') as posts:
        with open('./unique/'+file,'w') as unique:
            for line in posts:
                id, user = line.split('\t')[0], line.split('\t')[2]
                if id not in idList and user not in trollUserList:
                    idList.append(id)
                    unique.write(line)
                    unq += 1
                total += 1
                
print unq, total