import os, re
import nltk
import io

def getNodes(tree):
    myPhrases = []

    if type(tree) is nltk.tree.Tree:
        myPhrases.append(tree.leaves())

    return myPhrases

def verifyLabel(tree, label):
    if type(tree) is nltk.tree.Tree:
        for child in tree:
            if (type(child) is nltk.tree.Tree and child.label() == label):
                return getNodes(tree)

for file in os.listdir("corpus"):

    print file

    lines = io.open("corpus/" + file, 'r', encoding="utf-8")

    for line in lines:
        line = line.encode('ascii', 'ignore')
        line = line.replace('(','').replace(')','').replace(';','').replace('/','')

        # sentence segmenter
        sentences = nltk.sent_tokenize(line)

        grammar = """
        DATE:   {<IN><NNP>?<CD>(<,><CD>)?}
                {<NNP><CD><,><CD>}
        LOCATION: {<IN><NNP><,><NNP>*}
        SUBJECT:  {<DT>?<JJ>*<NN.*>+}
        PREDICATE:  {<V.*><V.*>?}
                    {<DT>?<JJ>*<NN.*>+}
        OBJECT: {<NN.*>}
        """
        cp = nltk.RegexpParser(grammar)

        pos_tags_aux = []
        for sent in sentences:
            # word tokenizer
            words = nltk.word_tokenize(sent)

            # apply part-of-speech tagger
            pos_tags = nltk.pos_tag(words)

            # parse grammar
            tree = cp.parse(pos_tags)

            print verifyLabel(tree, "DATE")

            pos_tags_aux.append(tree)
