import os
import nltk
import io

for file in os.listdir("corpus"):
    print file
    lines = io.open("corpus/" + file, 'r', encoding="utf-8")

    for line in lines:
        sentence = nltk.sent_tokenize(line)

        sentence = [nltk.word_tokenize(sent) for sent in sentence]

        sentence = [nltk.pos_tag(sent) for sent in sentence]

        grammar = "NP: {<DT>?<JJ>*<NN>}"
        print sentence

        cp = nltk.RegexpParser(grammar)
        result = cp.parse(sentence)

        print result