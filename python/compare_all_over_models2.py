import gensim
import sys
import collections
import codecs
import re
import math
from copy import deepcopy


def compare(models):
    words = {}
    counts = {}
    sim = {}
    rel = {}

    for i in range(len(models)):
        models[i] = gensim.models.Word2Vec.load_word2vec_format(
            models[i], binary=True)
    v = models[0].vocab 
    print(len(v))
    x = 0
    for word in v:
        for n in range(1, 6):
            if not n in rel:
                rel[n] = 0
            similar = [[w for w, s in model.most_similar(
                word, topn=n)] if word in model.vocab else [] for model in models]
            rel[n] += len(intersection(similar))
        x += 1
        if x % 1000 == 0:
            print(x)
            for n in range(1, 6):
                print(rel[n] / x, "@", n)
    for n in range(1, 6):
        rel[n] /= len(v)
    return rel


def intersection(sequences):
    if len(sequences) < 2:
        raise Exception("Need multiple sequences for comparisson")
    inter = set(sequences[0])
    for s in sequences[1:]:
        inter = inter.intersection(s)
    return inter


def main():
    if len(sys.argv) < 2:
        raise Exception(
            "Provide 1+ arguments:\n\t1+,model(s)")
    models = sys.argv[1:]

    reliability = compare(models)
    for n in range(1, 6):
        print(reliability[n], "@", n)

if __name__ == "__main__":
    main()
