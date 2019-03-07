import pandas as pd
import numpy as np
import sys
import math
import random
import matplotlib.pyplot as plt
import nltk.data
from nltk import tokenize
from os import listdir
import os.path
import re

prefixes = ['Mr.', 'Mrs.', 'Dr.', 'Ms.', 'Sir.', 'Jr.', 'Sr.', 'Gen.', 'Gov.', 'Prof.']

def read_input():
    if(len(sys.argv)!=3):
        sys.exit("ERROR: The program requires 1 input argument")
    else:
        dir_path = str(sys.argv[1])
        type_of_split = str(sys.argv[1])
        if type_of_split.lower() == "t" or type_of_split.lower() == "train":
            type_of_split = "train"
        elif type_of_split.lower() == "v" or type_of_split.lower().startswith("val"):
            type_of_split = "val"
        else:
            type_of_split = "test"

    return dir_path, type_of_split


def get_sentences(filename):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    fp = open(filename)
    data = fp.read()
    for i in range(len(prefixes)):
        data.replace(prefixes[i], prefixes[i][:-1])
    sentences = tokenize.sent_tokenize(data)
    return sentences

def get_all_elements(dir_path):
    word_list = []
    start_ind = []
    end_ind = []
    n_gram_count = []
    filename_list = []
    pre_string = []
    pos_string = []
    output_classes = []
    start_tag = '<name>'
    end_tag = '</name>'
    for fname in listdir(dir_path):
        fname = os.path.join(dir_path, fname)
        print(fname)
        index = 0
        line_sentences = get_sentences(fname)
        # print(len(line_sentences))

        for sent in line_sentences:
            sent = re.sub('[^0-9a-zA-Z>< \'\\/]+', '', sent)
            # print(sent)
            words = sent.split()
            words = list(filter(None, words))
            ngram_start = False
            for ngram in range(1,4):
                for i in range(len(words)+1-ngram):
                    actual_class = 0
                    # print(i)
                    # if(i<0):
                    #     continue
                    word = " ".join(words[i:i + ngram])
                    if(words[i].startswith(start_tag)):
                        ngram_start = True
                        print("start at :", words[i])
                    if ngram_start == True:
                        actual_class = 1
                        if end_tag in word and not(word.endswith(end_tag)):
                            actual_class = 0
                            print("marked label 0:"+word)
                    if (words[i].endswith(end_tag)):
                        ngram_start = False
                        print("end at :", word)



                    if(len(word)==0):
                        continue
                    word_list.append(word)
                    start_ind.append(i)
                    end_ind.append(i+ngram-1)
                    n_gram_count.append(ngram)
                    filename_list.append(fname)
                    pre_string.append(words[max(0,i-5):i])
                    pos_string.append(words[i+ngram: min(len(words), i+ngram+5)])
                    output_classes.append(actual_class)



    df = pd.DataFrame(data = {"Tokens":word_list, "filename":filename_list, "n-gram_count":n_gram_count, "start_ind":start_ind , "end_ind":end_ind, "pre_string":pre_string, "pos_string":pos_string, "output_classes":output_classes})
    return df





dir_path, type_of_split = read_input()
df = get_all_elements(dir_path)
df.to_csv("Tokenized"+type_of_split+".csv", sep = '_', index = False)