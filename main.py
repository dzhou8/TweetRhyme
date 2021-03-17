import json
from nltk.tokenize import sent_tokenize
import pronouncing
from random import randrange
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

fileName = 'trump.json'

file = open(fileName)
tweetDict = json.load(file)
text = ""
tweetsOnly = []
for tweet in tweetDict:
    if randrange(50) == 0:
        text += tweet["text"]

tweetsOnly = sent_tokenize(text)
print(len(tweetsOnly))

for tweet in tweetsOnly:
    if tweet.startswith('https://t.co/'):
        tweetsOnly.remove(tweet)

print(len(tweetsOnly))

lastWords = []
for tweet in tweetsOnly:
    lastWord = tweet.split()[-1].lower().strip("!?.")
    lastWords.append(lastWord)

n = len(lastWords)
edgeList = [[0]*n for i in range(n)]
for i in range(len(lastWords)):
    for j in range(len(lastWords)):
        if lastWords[i] in pronouncing.rhymes(lastWords[j]) and lastWords[j] in pronouncing.rhymes(lastWords[i]) and lastWords[i] != lastWords[j]:
            edgeList[i][j] = 1
            edgeList[j][i] = 1
print(n)

graph = csr_matrix(edgeList)
n_components, labels = connected_components(csgraph=graph, directed=False, return_labels=True)
print(n_components)

RhymeSet = []
for i in range(n_components):
    if (labels == i).sum() > 1:
        thisRhymeSet = []
        for j in range(n):
            if labels[j] == i:
                thisRhymeSet.append(tweetsOnly[j])
        RhymeSet.append(thisRhymeSet)

for s in RhymeSet:
    for t in s:
        print(t)
    print('break')