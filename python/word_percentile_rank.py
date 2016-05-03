import gensim
import sys
import collections
import codecs
import re
import math
from copy import deepcopy

bins = 100

def main():
    if len(sys.argv) < 2:
        raise Exception(
            "Provide 1+ arguments:\n\t1,model\n\t2+,word(s) - otherwise default list is used")
    model = gensim.models.Word2Vec.load_word2vec_format(
            sys.argv[1], binary=True)
    v = len(model.vocab)
    if len(sys.argv) > 2:
        words = sys.argv[2:]
    else:
        words = ["card", "sleep", "parent", "address", "gay", "mouse", "king", "checked", "check", "actually", "supposed", "guess", "cell", "headed", "ass", "mail", "toilet", "cock", "bloody", "nice", "guy"]
    for word in words:
        rank = model.vocab[word].index
        percentile_rank = int((rank * bins) / v)
        print(word+","+str(bins - 1 - percentile_rank))

if __name__ == "__main__":
    main()
