import glob
import codecs
import re
import gensim
import os
import time
import collections
import sys
import re
from gensim import matutils, corpora, models, similarities
from gensim.matutils import unitvec
from gensim.models.word2vec import Vocab
from numpy import dot, copy


import logging
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


class Corpus(object):
    """for structure of google books 2012 files"""

    def __init__(self, corpus_file, corpus_path):
        self.corpus_path = corpus_path
        self.corpus_file = corpus_file
        self.first = {}

    def __iter__(self):
        if not os.path.exists(os.path.join(self.corpus_path, self.corpus_file)):
            logging.info("skipping %s", self.corpus_file)
        else:
            for line in open(
                    os.path.join(
                        self.corpus_path,
                        self.corpus_file),
                    "r",
                    encoding="utf-8"):
                # one document per line, tokens separated by whitespace, tabs separate
                # year/counts
                if line == "\n":
                    continue
                text, year, match_count, volume_count = line.split("\t")
                text = text.lower().split(" ")
                for i in range(int(match_count)):
                    for word in text:
                        if not word in self.first:
                            self.first[word] = self.corpus_file
                    yield text


def update_vocab(corpus, old_model, model):
    """Like mode.build_vocab(), inserts words/vectors from old model"""
    count = model.min_count + 1
    model.scan_vocab(corpus)  # initial survey
    for word in old_model.vocab:  # insert old
        if word not in model.vocab:
            model.raw_vocab[word] += count
            model.vocab[word] = Vocab(
                count=count, index=len(model.index2word))
            model.index2word.append(word)
    # trim by min_count & precalculate downsampling
    model.scale_vocab()
    model.finalize_vocab()  # build tables & arrays
    for word in old_model.vocab:
        if word in model.vocab:
            model.syn0[model.vocab[word].index] = old_model.syn0[
                old_model.vocab[word].index]


def main():
    # model parameters, taken from Kim et al. & Kulkarni et al.
    ALPHA = 0.01
    NET_SIZE = 200

    if len(sys.argv) < 11:
        raise Exception("""Provide 5+ arguments:\n\t1,path to save models\n\t2,path to corpora
            \t3,number of worker processes\n\t4,number of max. epochs\n\t5, minimum count
            \t6, hierarchic (0/1)\n\t7,neg sampling (0-20)\n\t8,downsampling (0-0.00001)
            \n\t9,max distance for convergence as exponent (e.g., 2 corresponding to 10^-2), use 0 to indicate no limit
            \n\t10+ files to train on (one model per file)""")
    model_path = sys.argv[1]
    corpus_path = sys.argv[2]
    workers = int(sys.argv[3])
    epochs = int(sys.argv[4])
    min_count = int(sys.argv[5])
    hs = int(sys.argv[6])
    negative = int(sys.argv[7])
    sample = float(sys.argv[8])
    if sys.argv[9] == "0":
        max_dist = None
    else:
        max_dist = 1 - 10**(-1 * float(sys.argv[9]))
    files = sys.argv[10:]

    if not os.path.exists(model_path):
        os.makedirs(model_path)
    old_model = None
    for f in files:
        if not os.path.exists(os.path.join(corpus_path, f)):
            logging.info("skipping %s", f)
            continue
        logging.info("processing %s", f)
        model = gensim.models.Word2Vec(
            size=NET_SIZE, window=4, min_count=min_count, workers=workers, alpha=ALPHA, sg=1,
            hs=hs, negative=negative, sample=sample)  # skip-gram on!
        corpus = Corpus(f, corpus_path)

        if old_model:
            update_vocab(corpus, old_model, model)
        else:
            model.build_vocab(corpus)

        epoch = 0
        dist = 0
        while epoch < epochs and (max_dist == None or dist < max_dist):
            epoch += 1
            if epoch > 1:
                old_syn0 = copy(model.syn0)
            model.train(corpus)
            if epoch > 1 and not max_dist == None:
                dist = sum([dot(unitvec(model.syn0[i]), unitvec(
                    old_syn0[i])) for i in range(len(model.vocab))]) / len(model.vocab)
        old_model = model

        fname = os.path.join(model_path, "model" + f)
        fvocab = os.path.join(model_path, "vocab" + f)
        model.save_word2vec_format(fname, fvocab=fvocab, binary=True)
        logging.info("finished after %s epochs", epoch)

    # store_count(examples,model_path,"ngrams_per_year")
    # store_count(first,model_path,"first_occurrence")

if __name__ == "__main__":
    main()
