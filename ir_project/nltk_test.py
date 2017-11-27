import os
import nltk
import io

for file in os.listdir("corpus"):
    print file
    lines = io.open("corpus/" + file, 'r', encoding="utf-8")

    for line in lines:
        print(line)
        # sentence segmenter
        sentence = nltk.sent_tokenize(line)

        # word tokenizer
        sentence = [nltk.word_tokenize(sent) for sent in sentence]
        # apply part-of-speech tagger
        sentence = [nltk.pos_tag(sent) for sent in sentence]

        grammar = r"""NP:{<DT|PP\$>?<JJ>*<NN>}"""

        cp = nltk.RegexpParser(grammar)
        result = cp.parse(sentence[0])

        print result