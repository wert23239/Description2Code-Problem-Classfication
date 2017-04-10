import glob
import math
import sys
from collections import defaultdict 
from fractions import Fraction
import numpy as np



def export_dict(word_count,word_dictionary,file_name):
    with open(file_name, 'w') as f:
        f.write(str(word_count))
        f.write('\n')
        for word, value in word_dictionary.items():
            f.write(str(word)+" "+str(value))
            f.write('\n')



def gather_data(file_path):
    txt = glob.glob(file_path)
    word_dict = defaultdict(int)
    count = 0
    word_count = 0
    for textfile in txt:
        count += 1
        # if not Fold[0]<=count or not Fold[1]>=count:
        word_count = GatherWordCount(textfile, word_dict, word_count)
    return word_dict, word_count

def GatherWordCount(textfile, wordDict, wordCount):
    f = open(textfile, 'r')
    for line in f:
        words = line.split()
        for i in words: #go through all words and add to hashtable of current word
            wordCount += 1
            wordDict[i] += 1
            if wordDict[i] == 1: #Lapace-Smoothing
                wordDict[i] += .00001 #add K
    f.close()
    return wordCount

def TestData(line, PostiveTable, PostiveCount, NegativeTable, NegativeCount):
    positive_class = 0
    negative_class = 0
    words = line.split()
    for i in words: #go through all words and add to hashtable of current word
        positive_class += math.log(calculate_probabilty(PostiveTable, i, PostiveCount))
        negative_class += math.log(calculate_probabilty(NegativeTable, i, NegativeCount))
    #positive_class+= math.log(float(PostiveCount)/(float(PostiveCount)+float(NegativeCount)))
    #negative_class+= math.log(float(NegativeCount)/(float(PostiveCount)+float(NegativeCount)))
    # total=np.exp(positive_class)+np.exp(negative_class)
    # pos_percent = np.exp(positive_class)/total
    # neg_percent= np.exp(negative_class)/total
   #return [positive_class,negative_class]
    return [positive_class, negative_class]

def calculate_probabilty(wordTable, Word, TableCount):
    classifier = 0
    if wordTable[Word] == 0:
        classifier = (.00001+1)/(TableCount+len(wordTable))
    else:
        classifier = (wordTable[Word]+1)/(TableCount+len(wordTable))
    return classifier




def import_dict(file_name):
    f = open(file_name, 'r')
    word_count=0
    word_dict = defaultdict(int)
    for line in f:
        words = line.split()
        if(len(words)==1):
            word_count=words[0]
        else:
            word_dict[words[0]]=float(words[1])
    f.close()
    return word_dict,int(word_count)

def gather_data_test(file_path,positive_table,positive_count,
negative_table,negative_count,label,Fold):
    txt = glob.glob(file_path)
    count = 0
    correct=0
    results= defaultdict(int)
    #print(label)
    for textfile in txt:
        count += 1
        if Fold[0]<=count and count<=Fold[1]:
            current = TestData(textfile,positive_table,positive_count,negative_table,negative_count)
            if(current==label):
                correct += 1   
    return correct

# Fold=()
# #print(sys.argv[1],sys.argv[2])
# if sys.argv[1]!="fold1" and sys.argv[2]!="fold1":
# 	Fold=(0,232)
# elif sys.argv[1]!="fold2" and sys.argv[2]!="fold2":
# 	Fold=(233,465)
# else:
# 	Fold=(466,698)	
	
#print(Fold)	

PATHPOS = "train-pos.txt"
PATHNEG = "train-neg.txt"
WORD_DICT_POSITIVE, POSITIVECOUNT = gather_data(PATHPOS)
WORD_DICT_NEGATIVE, NegativeCount = gather_data(PATHNEG)
#print(POSITIVECOUNT)
#print(NegativeCount)
export_dict(POSITIVECOUNT, WORD_DICT_POSITIVE, "Postive.txt")
export_dict(NegativeCount, WORD_DICT_NEGATIVE, "Negative.txt")
resultspos=[]
resultsneg=[]
testpos = "test-pos.txt"
f = open(testpos, 'r')
for line in f:
    resultspos.append(TestData(line, WORD_DICT_POSITIVE, POSITIVECOUNT,WORD_DICT_NEGATIVE,NegativeCount)) 
f.close()
testneg = "test-neg.txt"
f = open(testneg, 'r')
for line in f:
    resultsneg.append(TestData(line, WORD_DICT_POSITIVE, POSITIVECOUNT,WORD_DICT_NEGATIVE,NegativeCount))
f.close()
poscount=0
negcount=0
poscorrect=0
negcorrect=0
for res in resultspos:
    poscount+=1
    if res[0]>res[1]:
        poscorrect+=1   
for res in resultsneg:
    negcount+=1
    if res[1]>res[0]:
        negcorrect+=1

print("The postive accuracy is "+str(poscorrect/float(poscount)))
print("The negative accuracy is "+str(negcorrect/float(negcount)))
print("The accuracy is "+str((poscorrect+negcorrect)/float(poscount+negcount)))
