import numpy
from stemming.porter2 import stem
from backend_client import backend_get_representation

# PARAM: sentences SENTENCE LIST
# PARAM: debugMode BOOLEAN DEBUG PURPOSES
def getWordToVectorMatrix(sentences,debugMode):
    word2Vec = numpy.zeros((len(sentences), len(sentences)))
    minval = 1.0
    maxval = 0.0
    argmin_i = 0
    argmin_j = 0
    argmax_i = 0
    argmax_j = 0

    for i in range(0, len(sentences)):
        sentEmdding1 = getSentenceEmbedding(sentences[i])
        for j in range(i, len(sentences)):
            sentEmdding2 = getSentenceEmbedding(sentences[j])
            score = 0.0
            if not (sentEmdding1 is None or sentEmdding2 is None):
                score = 0.5 * (numpy.dot(sentEmdding1, sentEmdding2)/numpy.sqrt(numpy.dot(sentEmdding1, sentEmdding1))*numpy.sqrt(numpy.dot(sentEmdding2, sentEmdding2))+1)
            word2Vec[i][j] = score
            word2Vec[j][i] = word2Vec[i][j]
            if i==j:
                continue
            if word2Vec[i][j] < minval:
                minval = word2Vec[i][j]
                argmin_i = i
                argmin_j = j
            if word2Vec[i][j] > maxval:
                maxval = word2Vec[i][j]
                argmax_i = i
                argmax_j = j

    for i in range(0, len(sentences)):
        for j in range(i+1, len(sentences)):
            normalized = (word2Vec[i][j]-minval)/(maxval-minval)
            word2Vec[i][j] = normalized
            word2Vec[j][i] = normalized

    for i in range(0, len(sentences)):
        word2Vec[i][i] = 0.0

    if(debugMode):
        print "maximally similar sentences (%d,%d) (score %f): \n  \"%s\"\n  \"%s\""%(argmax_i,argmax_j,word2Vec[argmax_i][argmax_j],' '.join(sentences[argmax_i]), ' '.join(sentences[argmax_j]))
        print "minimally similar sentences (%d,%d) (score %f): \n  \"%s\"\n  \"%s\""%(argmin_i,argmin_j,word2Vec[argmin_i][argmin_j],' '.join(sentences[argmin_i]), ' '.join(sentences[argmin_j]))

    return word2Vec

# THIS FUNCTION RETURNS THE EMBEDDING OF GIVEN SENTENCE
# PARAM: sentence STRING
def getSentenceEmbedding(sentence):
    sentence_embedding = 0.0
    count = 0.0
    for w in sentence:
        word = w.lower()
        word = filter(str.isalnum, word)
        wordrep = getEmbedding(word)
        if wordrep is None:
            wordrep = getEmbedding(stem(word))
        if wordrep is not None:
            sentence_embedding += wordrep
            count = count + 1.0
    if count == 0:
        return None
    return numpy.divide(sentence_embedding, count)

# THIS FUNCTION RETURNS THE EMBEDDING OF GIVEN WORD FROM BACKEND SERVER
# PARAM: word STRING
def getEmbedding(word):
    wordrep = backend_get_representation(word)
    return wordrep