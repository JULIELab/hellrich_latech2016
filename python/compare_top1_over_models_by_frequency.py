import gensim
import sys
import collections
import codecs
import re
import math
from copy import deepcopy

bins = 100

def compare(models):
    words = {}
    counts = {}
    sim = {}
    rel = {}

    for i in range(len(models)):
        models[i] = gensim.models.Word2Vec.load_word2vec_format(
            models[i], binary=True)
    v = models[0].vocab
    reliability = [0 for i in range(bins)]
    inside = [0 for i in range(bins)]

    for word in v:
        rank = models[0].vocab[word].index
        percentile_rank = int((rank * bins) / len(v))
        inside[percentile_rank] += 1
        reliability[percentile_rank] += len(intersection(
            [[word for word, sim in model.most_similar(word, topn=1)] if word in model.vocab else [] for model in models]))
    return [reliability[percentile_rank] / inside[percentile_rank] if inside[percentile_rank] > 0 else 0 for percentile_rank in range(bins)]


def intersection(sequences):
    if len(sequences) < 2:
        raise Exception("Need multiple sequences for comparisson")
    inter = set(sequences[0])
    for s in sequences[1:]:
        inter = inter.intersection(set(s))
    return inter


def main():
    if len(sys.argv) < 2:
        raise Exception(
            "Provide 1+ arguments:\n\t1+,model(s)")
    models = sys.argv[1:]

    reliability = compare(models)
    for i in range(0, bins):
        print(str((bins-1) - i)+","+str(reliability[i]))

if __name__ == "__main__":
    main()
