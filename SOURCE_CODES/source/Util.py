UNIT_WORDS           = 1
UNIT_SENTENCES       = 2
UNIT_CHARACTERS      = 3
import  os

def get_stopwords(stopwordsFilename):
    stopwords = list()
    f = open(stopwordsFilename, 'r')
    for line in f:
        stopwords.append(line)
    f.close()
    return stopwords

def getPositiveWords(positiveWordsFilename):
    f = open(os.path.dirname(__file__)+positiveWordsFilename)
    #positive_emotions = Set(f.readlines())
    positive_emotions = set()
    for pos in f.readlines():
        #print pos
        positive_emotions.add(pos.replace("\n", ""))
    return positive_emotions

def getnegativeWords(negativeWordsFilename):
    f = open(os.path.dirname(__file__)+negativeWordsFilename)
    negative_emotions = set()
    for neg in f.readlines():
        #print neg
        negative_emotions.add(neg.replace("\n", ""))
    return negative_emotions

def count_sentences(documents):
    lines = 0
    for document in documents:
        lines += len(document)
    return lines

def getSentenceFromIndex(i, documents):
    searchedLines = 0
    for document in documents:
        if searchedLines + len(document) > i:
            return document[i-searchedLines]
        else:
            searchedLines += len(document)
    return None

def characters_length(selected, documents):
    chars = 0
    for i in selected:
        sentence_chars = 0
        sentence = getSentenceFromIndex(i, documents)
        for word in sentence:
            # The +1 counts an implicit space between each word.
            sentence_chars += len(word)+1
        chars += sentence_chars
    return chars

def words_length(selected, documents):
    words = 0
    for i in selected:
        words += len(getSentenceFromIndex(i, documents))
    return words

def summaryShort(selected, documents, lengthUnit, summarySize):
    if lengthUnit == UNIT_CHARACTERS:
        return characters_length(selected, documents) < summarySize
    elif lengthUnit == UNIT_WORDS:
        return words_length(selected, documents) < summarySize
    else:
        return len(selected) < summarySize

def summaryLong(selected, documents, lengthUnit, summarySize):
    if lengthUnit == UNIT_CHARACTERS:
        return characters_length(selected, documents) > summarySize
    elif lengthUnit == UNIT_WORDS:
        return words_length(selected, documents) > summarySize
    else:
        return len(selected) > summarySize


