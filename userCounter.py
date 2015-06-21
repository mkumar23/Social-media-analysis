'''
Created on Mar 1, 2015

@author: Mrinal
'''
from os import listdir
from os.path import join as joinpath

path = './unique/posts'
userName = set()
doclist = [joinpath(path, fname) for fname in listdir(path) if fname.endswith('.txt')]
for file in doclist:
    with open(file,'r') as posts:
        for line in posts:
            userName |= set([line.split('\t')[2]])
            
print len(userName)