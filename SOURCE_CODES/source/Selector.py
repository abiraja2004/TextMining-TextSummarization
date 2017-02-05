import os

from MatrixAggregation import L1
from MatrixAggregation import R1
from Util import count_sentences
from Util import  summaryShort
from Util import summaryLong
from New import get_clustering
A                    = 5.0
DEFAULT_LAMBDA       = 6.0
from Clustering import getClusteringByVec
from Clustering import getK
DEFAULT_STOPWORDS   = os.path.split(os.path.realpath(__file__))[0]+'/english_stopwords.txt'

def selectSentences(summarySize,aggregateSimilartyMatrix,sentenceVectors,documents,lengthUnit,idfVectorFileName,docName,use_aggregate_for_clustering):

    selected = set()

    K = getK(count_sentences(documents))
    if use_aggregate_for_clustering:
        clustering = get_clustering(aggregateSimilartyMatrix)
    elif not sentenceVectors is None:
        clustering = getClusteringByVec(sentenceVectors, K, idfVectorFileName, docName)

    #print "Optimization loop:"
    while summaryShort(selected, documents, lengthUnit, summarySize):
        max_val = 0.0
        argmax = None
        for i in range(0,aggregateSimilartyMatrix.shape[0]):
            if i not in selected:# and i not in discarded:
                selected.add(i)
                curr = L1 (selected, aggregateSimilartyMatrix, None, A) + DEFAULT_LAMBDA * R1(selected, aggregateSimilartyMatrix, clustering, K)
                # as in Lin-Bilmes 2010: */
                #print(str(curr)+" "+str(max_val)+" "+str(argmax))
                if curr > max_val:
                    argmax = i
                    max_val = curr
                selected.remove(i)

        if argmax:
            selected.add(argmax) #internal: zero-based.
        else:
            break

    #print("zero-based set:  ")
    #print(selected)

    #MoD_SINGLETON:
    currentlyBestCScore = L1(selected, aggregateSimilartyMatrix, None, A) + DEFAULT_LAMBDA * R1(selected, aggregateSimilartyMatrix, clustering, K)
    currentlyBestSingleton = None
    for i in range(0,aggregateSimilartyMatrix.shape[0]):
        singleton = set()
        singleton.add(i)
        if not summaryLong(singleton, documents, lengthUnit, summarySize):
            singletonSummaryScore = L1(singleton, aggregateSimilartyMatrix, None, A) + DEFAULT_LAMBDA * R1(singleton, aggregateSimilartyMatrix, clustering, K)
            if singletonSummaryScore > currentlyBestCScore:
                currentlyBestCScore = singletonSummaryScore
                currentlyBestSingleton = i

    if currentlyBestSingleton:
        print("Using singleton!")
        selected = set()
        selected.add(currentlyBestSingleton)

    return selected