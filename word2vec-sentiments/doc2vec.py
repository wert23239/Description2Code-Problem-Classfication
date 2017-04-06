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

from sklearn.linear_model import LogisticRegression

def doc_convert(SIZE,MIN_COUNT,WINDOW,NEGATIVE_WORDS,EPOCH_SIZE):
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    sources = {'test-neg.txt':'TEST_NEG', 'test-pos.txt':'TEST_POS', 'train-neg.txt':'TRAIN_NEG', 'train-pos.txt':'TRAIN_POS', 'train-unsup.txt':'TRAIN_UNS'}

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

    sentences = LabeledLineSentence(sources)


    model = Doc2Vec(min_count=MIN_COUNT, window=WINDOW, size=SIZE, sample=1e-4, negative=5, workers=7)

    model.build_vocab(sentences.to_array())

    for epoch in range(EPOCH_SIZE):
        logger.info('Epoch %d' % epoch)
        model.train(sentences.sentences_perm())

    logger.info('Sentiment')
    train_arrays = numpy.zeros((381, SIZE))
    train_labels = numpy.zeros(381)

    for i in range(208):
        prefix_train_pos = 'TRAIN_POS_' + str(i)
        train_arrays[i] = model.docvecs[prefix_train_pos]
        train_labels[i] = 1
    for i in range(173):
        prefix_train_neg = 'TRAIN_NEG_' + str(i)
        train_arrays[208 + i] = model.docvecs[prefix_train_neg]
        train_labels[208 + i] = 0


    test_arrays = numpy.zeros((94, SIZE))
    test_labels = numpy.zeros(94)

    for i in range(54):
        prefix_test_pos = 'TEST_POS_' + str(i)
        test_arrays[i] = model.docvecs[prefix_test_pos]
        test_labels[i] = 1
    for i in range(40):
        prefix_test_neg = 'TEST_NEG_' + str(i)
        test_arrays[54 + i] = model.docvecs[prefix_test_neg]
        test_labels[54 + i] = 0

    logger.info('Fitting')
    classifier = LogisticRegression()
    classifier.fit(train_arrays, train_labels)

    LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
          intercept_scaling=1, penalty='l2', random_state=None, tol=0.0001)

    return 1-classifier.score(test_arrays, test_labels)


def main(job_id, params):
    SIZE=params['size'][0]
    MIN_COUNT=params['min_count'][0]
    WINDOW=params['window'][0]
    EPOCH_SIZE=params['epoch_size'][0]
    NEGATIVE_WORDS=params['negative'][0]
    #res = doc_convert(SIZE,MIN_COUNT,WINDOW,NEGATIVE_WORDS,EPOCH_SIZE)
    #print "Jonny's function in 2D:"
    #print "\tf(%.2f, %0.2f, %0.2f) = %f" % (learning_rate,beta_1,beta_2, res)
    return doc_convert(SIZE,MIN_COUNT,WINDOW,NEGATIVE_WORDS,EPOCH_SIZE)



if __name__ == "__main__":
    main(23, {'size': [100],'min_count': [3],'window': [10],'negative': [5],'epoch_size': [100]})


