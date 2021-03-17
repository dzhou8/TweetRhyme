# This program generates groups of rhyming tweets from a data file. For my poem, I just did Trump
# Code is lightly commented

#imports
import json
from nltk.tokenize import sent_tokenize
import pronouncing
from random import randrange
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

#filename with tweets here
fileName = 'trump.json'

#extract tweets from data file
file = open(fileName)
tweetDict = json.load(file)
text = ""
tweetsOnly = []
for tweet in tweetDict:
    if randrange(50) == 0: #we randomly select 2% of his tweets as he has too many to run my algorithm (can change this number)
        text += tweet["text"]

 #then we take the tweets and break them up into sentences
tweetsOnly = sent_tokenize(text)
print(len(tweetsOnly))

#remove all sentences that start with https://t.co/. This usually means he is just retweeting.
for tweet in tweetsOnly:
    if tweet.startswith('https://t.co/'):
        tweetsOnly.remove(tweet)

print(len(tweetsOnly))

#this gets the last word from each sentence (important in determining rhyme.
lastWords = []
for tweet in tweetsOnly:
    lastWord = tweet.split()[-1].lower().strip("!?.")
    lastWords.append(lastWord)

#this code builds a matrix of which last words rhyme with each other.
#Uses the prounouncing.rhymes library to determine rhyme quality
n = len(lastWords)
edgeList = [[0]*n for i in range(n)]
for i in range(len(lastWords)):
    for j in range(len(lastWords)):
        if lastWords[i] in pronouncing.rhymes(lastWords[j]) and lastWords[j] in pronouncing.rhymes(lastWords[i]) and lastWords[i] != lastWords[j]: #words don't rhyme with themselves (to reduce duplicates)
            edgeList[i][j] = 1
            edgeList[j][i] = 1
print(n)

#This code runs an algorithm to generate strongly connected components. That is, lines that all rhyme with each other.
graph = csr_matrix(edgeList)
n_components, labels = connected_components(csgraph=graph, directed=False, return_labels=True)
print(n_components)

#remaining code prints out all the rhyming groups, with 'break' in between
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