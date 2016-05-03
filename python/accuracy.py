import gensim
import sys
import collections
import codecs
import re
import math
from copy import deepcopy


def get_accuracy(test_file, models):
    for i in range(len(models)):
        models[i] = gensim.models.Word2Vec.load_word2vec_format(
            models[i], binary=True)
    acc = []
    for model in models:
        for section in model.accuracy(test_file):
            print(section["section"], len(section["correct"]), len(
                section["incorrect"]), len(section["correct"]) / (len(section["correct"]) + len(section["incorrect"])))
            if section["section"] == "total":
                acc.append(
                    len(section["correct"]) / (len(section["correct"]) + len(section["incorrect"])))
    average = sum(acc) / len(acc)
    sdev = math.sqrt(sum([(a - average)**2 for a in acc]) / len(acc))
    print(average, sdev)


def main():
    if len(sys.argv) < 3:
        raise Exception(
            "Provide 1+ arguments:\n\t1, test file\n\t2+,model(s)")
    test_file = sys.argv[1]
    models = sys.argv[2:]

    get_accuracy(test_file, models)

if __name__ == "__main__":
    main()
