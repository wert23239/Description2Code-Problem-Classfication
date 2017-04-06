
# coding: utf-8

# In[1]:

SIZE=49
MIN_COUNT=2
WINDOW=19
NEGATIVE_WORDS=1
EPOCH_SIZE=10


# In[2]:

# gensim modules
from gensim import utils
from gensim.models.doc2vec import LabeledSentence
from gensim.models import Doc2Vec

# numpy
import numpy

# shuffle
from random import shuffle

# logging
import logging
import os.path
import sys

model = Doc2Vec.load('./problems.d2v')


# In[20]:

print(model.most_similar('math'))