import os, io, re, nltk, patterns

keys = {'name':'', 'birth_date':'', 'birth_place': '', 'death_date':'',
            'death_place': '', 'occupation':'', 'nationality':'', 'genre':'',
            'notableworks':'', 'alma_mater':'', 'spouse':'', 'children':''}

def getPatternList(key):

    if key not in keys:
        raise ValueError("Wrong key")

    if key == 'birth_date':
        return patterns.pattern_birth_date
    elif key == 'birth_place':
        return patterns.pattern_birth_place
    elif key == 'death_date':
        return patterns.pattern_death_date
    elif key == 'death_place':
        return patterns.pattern_death_place


def filterSentenceByKey(sentence, key):
    pattern_list = getPatternList(key)

    if len(pattern_list) != 0:
        for pattern in pattern_list:
            pattern = re.compile(pattern)
            match = pattern.match(sentence)
            if match is not None:
                return match.group(0)


def consultCorpusByKey(key):
    for file in os.listdir("corpus"):
        print ">>> "+file

        keys['name'] = file

        file = io.open("corpus/" + file, 'r', encoding="utf-8")

        for line in file:
            line = line.encode('ascii', 'ignore')

            # sentence segmenter
            sentences = nltk.sent_tokenize(line)

            for sentence in sentences:

                sent = filterSentenceByKey(sentence, key)

                if sent is not None:
                    # word tokenizer
                    words = nltk.word_tokenize(sent)

                    # apply part-of-speech tagger
                    pos_tags = nltk.pos_tag(words)

                    # chunk entities
                    chunked_sentence = nltk.ne_chunk(pos_tags)

                    #print chunked_sentence

                    pattern = """.*"""
                    pattern = re.compile(pattern)
                    for r in nltk.sem.relextract.extract_rels('PERSON', 'LOCATION', chunked_sentence, corpus='ace', pattern=pattern):
                        print(nltk.sem.relextract.rtuple(r))

consultCorpusByKey("birth_place")