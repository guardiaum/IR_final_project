import os, io, re, nltk, patterns
import pandas as pd
from nltk.sem.relextract import extract_rels, rtuple


keys = {'name':'', 'birth_date':'', 'death_date':'', 'birth_place': '', 'death_place':'',
        'nationality': '', 'partner':[], 'alma_mater':[], 'occupation':'', 'genre':[]}


def generateChunkByGrammar(tags, grammar):
    rp = nltk.RegexpParser(grammar)
    return rp.parse(tags)


def generateNLTKChunk(tags):
    chunked_sentence = nltk.ne_chunk(tags)
    return chunked_sentence


def verifyLabelInTags(tags, words):
    for tag in tags:
        if tag[0] in words:
            return True
    return False


def getValueByKey(author_name, tags, key):

    if key == 'birth_date' or key == 'death_date':
        grammar = """DATE: {<CD><NNP><CD>}
                           {<NNP><CD><,><CD>}"""

        tree = generateChunkByGrammar(tags, grammar)

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
        authorFound = verifyLabelInTags(tags, author_name)

        if authorFound:
            tree = generateNLTKChunk(tags)

            if type(tree) is nltk.tree.Tree:
                value = ''
                for node in tree:
                    if type(node) is nltk.tree.Tree:
                        if node.label() == 'GPE':
                            for leaf in node.leaves():
                                if leaf[1] == 'JJ':
                                    value = leaf[0] + ' '
                return value

    elif key == 'partner':
        authorFound = verifyLabelInTags(tags, author_name) | \
                      verifyLabelInTags(tags, 'her') |  \
                      verifyLabelInTags(tags, 'his') | \
                      verifyLabelInTags(tags, 'he') | \
                      verifyLabelInTags(tags, 'she')

        if authorFound:
            grammar = """MARRIED: {(<PRP>|<NNP>+|<VBG>)(<VBD>|<JJ>|(<VBN><IN>))<NNP>+}"""

            tree = generateChunkByGrammar(tags, grammar)
            #print tree
            for node in tree:
                if type(node) is nltk.tree.Tree:
                    if node.label() == 'MARRIED':
                        value = ''
                        for leaf in node.leaves():
                            value += leaf[0] + ' '
                        return value

    elif key == 'alma_mater':
        tagFound = verifyLabelInTags(tags, author_name) |\
                   verifyLabelInTags(tags, 'in') | \
                   verifyLabelInTags(tags, 'the') | \
                   verifyLabelInTags(tags, 'attended') | \
                   verifyLabelInTags(tags, 'graduated')


        if(tagFound):
            grammar = """ATTENDED: {(<VBD>|<VBN><DT>|<IN><DT>?)<NNP>+}
                                    {<VBD><NNP><IN><NNP>}
                                    {(<VBD>|<VBN>)<NNP>+}
                                    {<IN><DT><NNP>+}"""

            tree = generateChunkByGrammar(tags, grammar)

            #print tree
            for node in tree:
                if type(node) is nltk.tree.Tree:
                    if node.label() == 'ATTENDED':
                        value = ''
                        for leaf in node.leaves():
                            value += leaf[0] + ' '
                        return value

    elif key == 'occupation':

        authorFound = verifyLabelInTags(tags, author_name)

        if authorFound:
            grammar = """OCCUPATION: {(<VBD>|<VBZ>)(<DT>?<JJ>?<NN>?<,>?<CC>?)*}"""

            tree = generateChunkByGrammar(tags, grammar)

            for node in tree:
                if type(node) is nltk.tree.Tree:
                    if node.label() == 'OCCUPATION':
                        value = ''
                        for leaf in node.leaves():
                            value += leaf[0] + ' '
                        return value


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
    elif key == 'partner':
        return patterns.pattern_partner
    elif key == 'occupation':
        return patterns.pattern_occupation
    elif key == 'alma_mater':
        return patterns.pattern_alma_mater
    elif key == 'genre':
        return patterns.pattern_genre


def filterSentenceByKey(sentence, key):
    pattern_list = getPatternList(key)

    if len(pattern_list) != 0:

        for pattern in pattern_list:
            p = re.compile(pattern)

            if key == 'genre':
                match = p.search(sentence)
                if match is not None:
                    return match.group(0)
            else:
                match = p.match(sentence)

                if match is not None:
                    return match.group(0)


def getFieldByKey(author_name, sentence, article_keys, key):

    sent = filterSentenceByKey(sentence, key)

    if sent is not None:

        if key == 'genre': # does not pos tag for genre field

            if sent not in article_keys[key]:
                article_keys[key].append(sent)
            return article_keys

        else:
            # word tokenizer
            words = nltk.word_tokenize(sent)

            # apply part-of-speech tagger
            pos_tags = nltk.pos_tag(words)

        if key == 'partner' or key == 'alma_mater':

            result = getValueByKey(author_name, pos_tags, key)

            if result != '' and result is not None and result not in article_keys[key]:
                article_keys[key].append(result)
                return article_keys

        elif article_keys[key] == '' and pos_tags is not None:

            result = getValueByKey(author_name, pos_tags, key)

            if result != '' or result is not None:
                article_keys[key] = result
                return article_keys


def fillFields():

    articles_fields = []

    for file_name in os.listdir("corpus"):

        article_keys = {'name': '', 'birth_date': '', 'death_date': '', 'birth_place': '', 'death_place': '',
                        'nationality': '', 'partner': [], 'alma_mater': [], 'occupation': '', 'genre': []}

        print ">>> "+file_name

        article_keys['name'] = file_name

        aux_article_keys = dict(article_keys)

        del aux_article_keys['name']

        file = io.open("corpus/" + file_name, 'r', encoding="utf-8")

        for line in file: # each line is a paragraph
            line = line.encode('ascii', 'ignore')

            # sentence segmenter
            sentences = nltk.sent_tokenize(line)

            for sentence in sentences:
                for key in aux_article_keys:
                    result = getFieldByKey(file_name, sentence, aux_article_keys, key)
                    if result is not None:
                        article_keys = result

        if article_keys is not None:
            article_keys['name'] = file_name
            articles_fields.append(article_keys)
            print article_keys

    dfs = []
    for article_keys in articles_fields:
        new_df = pd.DataFrame([article_keys], columns=['name', 'birth_date', 'death_date',
                                                       'birth_place', 'death_place', 'nationality',
                                                       'partner', 'alma_mater', 'occupation', 'genre'])
        dfs.append(new_df)

    dfs = pd.concat(dfs, ignore_index=True)

    dfs.to_csv('output.csv', index=True)

fillFields()