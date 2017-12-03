import os, io, re, nltk, patterns

keys = {'name':'', 'birth_date':'', 'death_date':'', 'birth_place': '', 'death_place':'',
        'nationality': ''}

'''keys = {'name':'', 'birth_date':'', 'birth_place': '', 'death_date':'',
            'death_place': '', 'occupation':'', 'nationality':'', 'genre':'',
            'notableworks':'', 'alma_mater':'', 'spouse':'', 'children':''}
            '''


def getValueByKey(tags, key):

    if key == 'birth_date' or key == 'death_date':
        grammar = """DATE: {<CD><NNP><CD>}
                           {<NNP><CD><,><CD>}"""

        tree = generateChunkByGrammar(tags, grammar)

        if type(tree) is nltk.tree.Tree:
            for node in tree:
                if type(node) is nltk.tree.Tree:

                    if node.label() == 'DATE':
                        value = ''
                        for leaf in node.leaves():
                            value += leaf[0] + ' '
                        return value

    elif key == 'birth_place' or key == 'death_place':

        tree = generateNLTKChunk(tags)

        if type(tree) is nltk.tree.Tree:
            value = ''
            for node in tree:
                if type(node) is nltk.tree.Tree:
                    if node.label() == 'GPE':
                        for leaf in node.leaves():
                            if leaf[1] == 'NNP':
                                value += leaf[0] + ' '
            return value
    elif key == 'nationality':

        tree = generateNLTKChunk(tags)

        if type(tree) is nltk.tree.Tree:
            value = ''
            for node in tree:
                if type(node) is nltk.tree.Tree:
                    if node.label() == 'GPE':
                        for leaf in node.leaves():
                            if leaf[1] == 'JJ':
                                value += leaf[0] + ' '
            return value


def generateChunkByGrammar(tags, grammar):
    rp = nltk.RegexpParser(grammar)
    return rp.parse(tags)


def generateNLTKChunk(tags):
    chunked_sentence = nltk.ne_chunk(tags)
    return chunked_sentence


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
    elif key == 'nationality':
        return patterns.pattern_nationality


def filterSentenceByKey(sentence, key):
    pattern_list = getPatternList(key)

    if len(pattern_list) != 0:
        for pattern in pattern_list:
            pattern = re.compile(pattern)
            match = pattern.match(sentence)
            if match is not None:
                return match.group(0)


def fillFields():

    for file_name in os.listdir("corpus"):

        article_keys = dict(keys)
        print ">>> "+file_name

        article_keys['name'] = file_name

        aux_article_keys = dict(article_keys)

        del aux_article_keys['name']

        file = io.open("corpus/" + file_name, 'r', encoding="utf-8")

        filled_keys = dict()
        for line in file: # each line is a paragraph
            line = line.encode('ascii', 'ignore')

            # sentence segmenter
            sentences = nltk.sent_tokenize(line)

            for sentence in sentences:
                for key in aux_article_keys:
                    result = getFieldByKey(sentence, aux_article_keys, key)
                    if result is not None:
                        filled_keys = result

        if filled_keys is not None:
            filled_keys['name'] = file_name
            print filled_keys


def getFieldByKey(sentence, article_keys, key):
    sent = filterSentenceByKey(sentence, key)

    if sent is not None:
        # word tokenizer
        words = nltk.word_tokenize(sent)

        # apply part-of-speech tagger
        pos_tags = nltk.pos_tag(words)

        if article_keys[key] == '':

            result = getValueByKey(pos_tags, key)

            if result != '':
                article_keys[key] = result
                return article_keys

fillFields()