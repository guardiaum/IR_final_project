import os
import nltk
import io

for file in os.listdir("corpus"):
    print file
    lines = io.open("corpus/" + file, 'r', encoding="utf-8")

    for line in lines:
        # sentence segmenter
        sentence = nltk.sent_tokenize(line)

        # word tokenizer
        sentence = [nltk.word_tokenize(sent) for sent in sentence]
        # apply part-of-speech tagger
        sentence = [nltk.pos_tag(sent) for sent in sentence]

        grammar = r"""NP:{<NNP>* <VBN> <NNP>*}"""

        cp = nltk.RegexpParser(grammar)
        if(len(sentence)>0):
            tree = nltk.tree(sentence[0])
            print tree