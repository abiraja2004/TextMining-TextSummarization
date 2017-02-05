from stemming.porter2 import stem
import math

# THIS METHOD RETURNS UNIGRAMS AND BIGRAMS AND ELIMINNATES STOP WORDS
def getUnigramAndBigrams(documents, stopwords):
    sentence_bag_list = list()

    first = True
    for document in documents:
        for sentence in document:

            current_sentence = dict()
            if len(sentence) > 0:

                prev = None
                for w in sentence:
                    w = filter(str.isalnum, w)
                    if not w:
                        continue
                    stemmed = stem(w)
                    if prev:
                        bigram = prev+" "+stemmed
                        current_sentence[bigram] = current_sentence.get(bigram,0)+1
                        #end, bigrams

                    if w not in stopwords:
                        current_sentence[stemmed] = current_sentence.get(stemmed,0)+1
                        prev = stemmed
                    else:
                        prev = w

            sentence_bag_list.append(current_sentence)
            first = False
    return sentence_bag_list

# THIS METHOD CALCULATES IDF SCORES FOR EACH UNIGRAM AND BIGRAM
def calculateUnigramAndBigramIDFScores(documents, stopwords):
    documentCountsForTerm = dict() # dictfrom string to integer

    if len(documents) <= 1:
        newCluster = list()
        document = documents[0]
        for s in document:
            l = list()
            l.append(s)
            newCluster.append(l)

        documents = newCluster

    for document in documents:
        curDoc = set()
        for sentence in document:
            if len(sentence) > 0:

                prev = None
                for w in sentence:
                    w = w.replace("_", "").replace(".", "").replace(",", "").replace("!", "").replace("?", "").replace("-", "")
                    if not w:
                        continue

                    w = w.lower()
                    stemmed = stem(w)

                    if prev:
                        curDoc.add(prev+" "+stemmed)

                    if w not in stopwords:
                        curDoc.add(stemmed)
                        prev = stemmed
                    else:
                        prev = w

        for term in curDoc:
            documentCountsForTerm[term] = documentCountsForTerm.get(term, 0)+1


    idfs = dict()
    for term in documentCountsForTerm:
        idfs[term] = math.log(len(documents)/documentCountsForTerm[term], 10)

    #print("Done calculating IDFS.")
    return idfs