import gensim
import sys
import collections
import codecs
import re
import math
from copy import deepcopy


def compare(word, topn, models, min_occ):
    words = {}
    counts = {}
    sim = {}
    for m in models:
        # replace last model with vocab
        fvocab = "vocab".join(m.rsplit("model", 1))
        model = gensim.models.Word2Vec.load_word2vec_format(
            m, fvocab=fvocab, binary=True)
        words[m] = []
        for iword, sim in model.most_similar(word, topn=topn * 10):
            if model.vocab[iword].count >= min_occ:
                words[m].append(iword)
        if len(words[m]) > topn:
            words[m] = words[m][:topn]
    return words


def common_with_limit(sequences, divider=2):
    if len(sequences) < 2:
        raise Exception("Need multiple sequences for comparisson")
    if divider == 0:
        raise Exception("Illegal divider 0")

    limit = math.floor(max([len(s) for s in sequences]) / divider)
    common = []

    rest = sequences[1:]
    assigned = [[] for i in range(len(rest))]

    for i, entry in enumerate(sequences[0]):
        matches = []
        # check for each sequence
        for sequence_id, sequence in enumerate(rest):
            left = int(max(0, i - limit))
            right = int(min(i + limit + 1, len(sequence)))
            for j in range(left, right):
                if j not in assigned[sequence_id] and sequence[j] == entry:
                    matches.append(j)
                    break
        if len(matches) == len(rest):
            common.append(entry)
            for sequence_id in range(len(rest)):
                assigned[sequence_id].append(matches[sequence_id])
    return common


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
            "Provide 2+ arguments:\n\t1,word\n\t2,minimum occ for related\n\t3+,model(s)")
    word = sys.argv[1].lower()
    min_occ = int(sys.argv[2])
    models = sys.argv[3:]

    words = compare(word, 20, models, min_occ)
    for key in words:
        print(words[key])
    for i in [5, 10, 20]:
        ws = [words[key][:i] for key in words]
        common = common_with_limit(ws)
        print("common:", common, "--->", len(common), "@", i)
        inter = intersection(ws)
        print("intersection:", inter, "--->", len(inter), "@", i)

if __name__ == "__main__":
    main()
