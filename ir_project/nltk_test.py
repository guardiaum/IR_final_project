import os, re
import nltk
import io

for file in os.listdir("corpus"):

    print file

    lines = io.open("corpus/" + file, 'r', encoding="utf-8")

    for line in lines:
        line = line.encode('ascii', 'ignore')
        line = line.replace('(','').replace(')','').replace(';','')

        # sentence segmenter
        sentences = nltk.sent_tokenize(line)

        # word tokenizer
        words = [nltk.word_tokenize(sent) for sent in sentences]

        # apply part-of-speech tagger
        pos_tags = [nltk.pos_tag(word) for word in words]

        #chunked_sentences = nltk.ne_chunk_sents(pos_tags, binary=True)
        chunked_sentences = [nltk.ne_chunk(pos_tag) for pos_tag in pos_tags]
        #print chunked_sentences
        '''
        pattern = """
        (partner(ed)|spouse|
        wife|husband|
        fiance|father|mother|
        child(ren)|marr(y|ied)|
        daughter|\bson\b)"""
        '''
        pattern = """born(ed)"""
        #pattern = """.*"""
        pattern = re.compile(pattern)

        for chunked_sentence in chunked_sentences:
            # 'ace': ['LOCATION', 'ORGANIZATION', 'PERSON', 'DURATION', 'DATE', 'CARDINAL', 'PERCENT', 'MONEY', 'MEASURE', 'FACILITY', 'GPE'],
            for r in nltk.sem.relextract.extract_rels('PERSON', 'DATE', chunked_sentence, corpus='ace', pattern=pattern):
                #print(r)
                print(nltk.sem.relextract.rtuple(r))