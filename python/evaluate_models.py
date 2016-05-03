import gensim
import sys
import collections
import codecs
import re
import math
from copy import deepcopy


def get_reliability(models):
    rel = {}
    v = set()
    for model in models:
        v = v.union(model.vocab)
    for word in v:
        similar = [[w for w, s in model.most_similar(
            word, topn=5)] if word in model.vocab else [] for model in models]
        for n in range(1, 6):
            if not n in rel:
                rel[n] = 0
            rel[n] += len(intersection(similar, n))
    for n in range(1, 6):
        rel[n] /= len(v)
    return rel


def intersection(sequences, n):
    if len(sequences) < 2:
        raise Exception("Need multiple sequences for comparisson")
    inter = set(sequences[0][:n])
    for s in sequences[1:]:
        inter = inter.intersection(s[:n])
    return inter


def get_accuracy(test_file, models):
    acc = []
    for model in models:
        for section in model.accuracy(test_file):
            if section["section"] == "total":
                acc.append(
                    len(section["correct"]) / (len(section["correct"]) + len(section["incorrect"])))
    average = sum(acc) / len(acc)
    sdev = math.sqrt(sum([(a - average)**2 for a in acc]) / len(acc))
    return (average, sdev)


def main():
    if len(sys.argv) < 3:
        raise Exception(
            "Provide 1+ arguments:\n\t1, test file\n\t2+,model(s)")
    test_file = sys.argv[1]
    models = [gensim.models.Word2Vec.load_word2vec_format(
        name, binary=True) for name in sys.argv[2:]]

    reliability = get_reliability(models)
    acc = get_accuracy(test_file, models)

    print(" & ".join(["{:.2f}".format(reliability[n] / n)
                      for n in range(1, 6)] + ["{:.2f}".format(acc[0]), "{:.2f}".format(acc[1])]))

if __name__ == "__main__":
    main()
