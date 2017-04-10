
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
import cPickle as pickle

program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)
logger.info("running %s" % ' '.join(sys.argv))


# In[3]:



class LabeledLineSentence(object):

    def __init__(self, sources):
        self.sources = sources

        flipped = {}

        # make sure that keys are unique
        for key, value in sources.items():
            if value not in flipped:
                flipped[value] = [key]
            else:
                raise Exception('Non-unique prefix encountered')

    def __iter__(self):
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    yield LabeledSentence(utils.to_unicode(line).split(), [prefix + '_%s' % item_no])

    def to_array(self):
        self.sentences = []
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    self.sentences.append(LabeledSentence(
                        utils.to_unicode(line).split(), [prefix + '_%s' % item_no]))
        return self.sentences

    def sentences_perm(self):
        shuffle(self.sentences)
        return self.sentences
sources = {'test-neg.txt':'TEST_NEG', 'test-pos.txt':'TEST_POS', 'train-neg.txt':'TRAIN_NEG', 'train-pos.txt':'TRAIN_POS', 'train-unsup.txt':'TRAIN_UNS'}

sentences = LabeledLineSentence(sources)


model = Doc2Vec(min_count=MIN_COUNT, window=WINDOW, size=SIZE, sample=1e-4, negative=5, workers=7)

model.build_vocab(sentences.to_array())





# In[4]:

for epoch in range(EPOCH_SIZE):
    logger.info('Epoch %d' % epoch)
    model.train(sentences.sentences_perm())


# In[5]:

model.save('./problems.d2v')


# In[6]:

model = Doc2Vec.load('./problems.d2v')


# In[7]:

model.most_similar('binary')


# In[8]:

model.docvecs['TRAIN_POS_0']


# In[9]:

model.docvecs['TEST_POS_0']


# In[10]:

logger.info('Sentiment')
train_arrays = numpy.zeros((210+154, SIZE))
train_labels = numpy.zeros(210+154)

for i in range(210):
    prefix_train_pos = 'TRAIN_POS_' + str(i)
    train_arrays[i] = model.docvecs[prefix_train_pos]
    train_labels[i] = 1
for i in range(154):
    prefix_train_neg = 'TRAIN_NEG_' + str(i)
    train_arrays[210 + i] = model.docvecs[prefix_train_neg]
    train_labels[210 + i] = 0


# In[11]:

test_arrays = numpy.zeros((52+38, SIZE))
test_labels = numpy.zeros(52+38)

for i in range(52):
    prefix_test_pos = 'TEST_POS_' + str(i)
    test_arrays[i] = model.docvecs[prefix_test_pos]
    test_labels[i] = 1
for i in range(38):
    prefix_test_neg = 'TEST_NEG_' + str(i)
    test_arrays[52 + i] = model.docvecs[prefix_test_neg]
    test_labels[52 + i] = 0


# In[12]:

from sklearn.linear_model import LogisticRegression

logger.info('Fitting')
classifier = LogisticRegression()
classifier.fit(train_arrays, train_labels)

LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
          intercept_scaling=1, penalty='l2', random_state=None, tol=0.0001)

print classifier.score(test_arrays, test_labels)


# In[15]:

from sklearn import svm
classifier = svm.SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
    decision_function_shape=None, degree=3, gamma='auto', kernel='rbf',
    max_iter=-1, probability=False, random_state=None, shrinking=True,
    tol=0.001, verbose=False)
classifier.fit(train_arrays, train_labels)
print(len(test_arrays))

print classifier.score(test_arrays,test_labels)


# In[14]:

svm.SVR()

