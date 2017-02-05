import numpy,math
from NgramExtractor import getUnigramAndBigrams
from NgramExtractor import calculateUnigramAndBigramIDFScores

def getTfIdfValues(documents, stopwords):

    sentences_bags = getUnigramAndBigrams(documents,stopwords)

    vocabulary_s = set() #list of strings
    for sentence in sentences_bags:
        for term in sentence:
            vocabulary_s.add(term)

    vocabulary = list(vocabulary_s)
    vocabulary.sort()

    vocabularyIndices = dict()
    for i in range(0,len(vocabulary)):
        vocabularyIndices[vocabulary[i]] = i

    sentenceTFIDFVectors = numpy.zeros((len(vocabulary),len(sentences_bags)))
    sentenceIDFVectors = numpy.zeros((len(vocabulary),len(sentences_bags)))


    idfs = calculateUnigramAndBigramIDFScores(documents, stopwords)

    tfidfden = numpy.zeros((len(sentences_bags)))
    idfden = numpy.zeros((len(sentences_bags)))
    for i in range(0, len(sentences_bags)):
        for term in sentences_bags[i]:
            tf = sentences_bags[i][term]
            idf = idfs.get(term,None)

            if not idf:
                idf = 1.0
                idfs[term] = idf

            tfidf = tf*idf

            sentenceTFIDFVectors[vocabularyIndices[term]][i] = tfidf
            sentenceIDFVectors[vocabularyIndices[term]][i] = idf

            tfidfden[i] += tfidf * tfidf
            idfden[i] += idf * idf

        tfidfden[i] = math.sqrt(tfidfden[i])
        idfden[i] = math.sqrt(idfden[i])

    tfidfsim = numpy.eye(len(sentences_bags))
    idfdist = numpy.zeros((len(sentences_bags),len(sentences_bags)))
    sentenceTFIDFEuclidean = numpy.zeros((len(sentences_bags),len(sentences_bags)))

    for i in range(0,len(sentences_bags)):
        for j in range(0,len(sentences_bags)):
            euclideanSum = 0.0; tfidfnum = 0.0; idfnum = 0.0
            for term in sentences_bags[i]:
                tf_i = sentences_bags[i].get(term,0)
                tf_j = sentences_bags[j].get(term,0)
                idf = idfs[term]
                if not idf:
                    idf = 1.0
                    idfs[term] = idf
                    print("No idf for "+term+"! ")

                euclideanSum += math.pow(tf_i*idf-tf_j*idf, 2)

                tfidf_i = tf_i*idf
                tfidf_j = tf_j*idf
                tfidfnum += tfidf_i * tfidf_j
                idfnum += idf * idf

            if tfidfden[i]==0 or tfidfden[j]==0:
                tfidfsim[i][j] = tfidfsim[j][i] = 0.0
            else:
                tfidfsim[i][j] = tfidfsim[j][i] = tfidfnum / (tfidfden[i] * tfidfden[j])
            if idfden[i]==0 or idfden[j]==0:
                idfdist[i][j] = idfdist[j][i] = 1.0
            else:
                idfdist[i][j] = idfdist[j][i] = 1.0 - idfnum / (idfden[i] * idfden[j])
            sentenceTFIDFEuclidean[i][j] = sentenceTFIDFEuclidean[j][i] = math.sqrt(euclideanSum)

    returnDictionary = dict()
    returnDictionary["tfidf_cosine"] = tfidfsim
    returnDictionary["tfidf_euclidean"] = sentenceTFIDFEuclidean
    returnDictionary["idf_dist"] = idfdist
    returnDictionary["idf_vectors"] = sentenceIDFVectors
    returnDictionary["tfidf_vectors"] = sentenceTFIDFVectors

    return returnDictionary