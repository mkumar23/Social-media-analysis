'''
Created on Feb 23, 2015

@author: Mrinal
'''
from _collections import defaultdict
prefile = 'PreModelledTopicAvoid14days'
postfile = 'PostModelledTopicAvoid14days'

def getTopicList(file):
    topic = []
    with open(file, 'r') as t:
        for line in t:
            topic.append(set(line.strip().split('\t')[1:]))
    
    return topic

pretopic = getTopicList(prefile)         
postTopic = getTopicList(postfile)

similarity = defaultdict(int)
for i in range(len(pretopic)):
    similarity[i] = defaultdict(int)
avgSimilarity = [0]*len(pretopic)
for i,t1 in enumerate(pretopic):
    for j,t2 in enumerate(postTopic):
        similarity[i][j] = len(t1 & t2)*1.0 / len(t1 | t2)
        avgSimilarity[i] += similarity[i][j]
    avgSimilarity[i] = avgSimilarity[i]*1.0/len(pretopic)    


with open('similarityMatrixAvoid', 'w') as sim:
    sim.write("Similarity Matrix: \n\n\n")
    for i in range(len(pretopic)):
        txt = ''
        for j in range(len(postTopic)):
            txt += str(similarity[i][j]) + '\t'
        sim.write(txt+'\n')
    
    txt = ''
    sim.write("\n\n\nAverage Similarity: \n\n\n")
    for i in range(len(avgSimilarity)):
        txt += str(avgSimilarity[i]) + '\t'
    sim.write(txt+'\n')
        