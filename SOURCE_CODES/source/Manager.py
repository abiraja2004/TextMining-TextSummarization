from Preprocess import preprocess
from TfIdfCalculator import getTfIdfValues
from Matrix import getWordToVectorMatrix
from Sentiment import  analyzeSentiment
from Selector import  selectSentences
from MatrixAggregation import calcAggregateSimMatrix

from graph import parseDirectedGraph
from ranker import rankMe
from sentencepickerMMR import cutListByNumberOfWords

# SENTIMENT ANALYSIS INCLUSIONS #####
from Util import  getSentenceFromIndex
from Util import  getPositiveWords
from Util import  getnegativeWords

unit = 1
femaleNamesFileName = "config/female_names.txt"
maleNamesFileName = "config/male_names.txt"
positiveSentimentFileName = "/config/emotion_words_positive.txt"
negativeSentimentFileName = "/config/emotion_words_negative.txt"
######

# SUMMARIZE GIVEN DOCUMENT LIST AND RETURNS SUMMARY STRING
# PARAM: documents MULTIDOCUMENT LIST
# PARAM: stopwords STOPWORD LIST
# PARAM: useTfIdfSimilarity BOOLEAN
# PARAM: useSentimentSimilarity BOOLEAN
# PARAM: useWordModel BOOLEAN
# PARAM: usePageRank BOOLEAN
# PARAM: useAggregateClustering BOOLEAN
# PARAM: length INTEGER
# PARAM: anaphoraResolution BOOLEAN
# PARAM: alphaValueForPagerank FLOAT
# PARAM: alphaValueForMMR FLOAT
# PARAM: debugMode BOOLEAN
def summarizeDocuments(documents, stopwords, useTfIdfSimilarity, useSentimentSimilarity, useWordModel, usePageRank, useAggregateClustering, length, anaphoraResolution, alphaValueForPagerank, alphaValueForMMR,debugMode):

    documents = preprocess(documents, femaleNamesFileName, maleNamesFileName, anaphoraResolution, debugMode)
    sentenceSimilarities = getTfIdfValues(documents, stopwords)

    matrices = list()
    flat_sentences = [sentence for document in documents for sentence in document]

    if useSentimentSimilarity:
        positiveWords = getPositiveWords(positiveSentimentFileName)
        negativeWords = getnegativeWords(negativeSentimentFileName)
        (pos, neg) = analyzeSentiment(flat_sentences,positiveWords,negativeWords,debugMode)
        matrices.append(pos)
        matrices.append(neg)

    if useWordModel:
        word2Vec = getWordToVectorMatrix(flat_sentences,debugMode)
        matrices.append(word2Vec)

    if useTfIdfSimilarity or len(matrices) == 0:
        matrices.append(sentenceSimilarities["tfidf_cosine"])
    # USE THE MATRICES LIST TO COMBINE THEM BY MULTIPLICATION ACCORDING TO SELECTION
    aggregateSimilartyMatrix = calcAggregateSimMatrix(matrices)

    # DETERMINE WHETHER PAGERANK OR CLUSTERING ALGORITHM
    if(usePageRank):
        output = usePageRankImplementation(documents,aggregateSimilartyMatrix,length,alphaValueForPagerank,alphaValueForMMR,debugMode)
    else:
        output = useClusteringAlgorithm(documents,aggregateSimilartyMatrix,length,sentenceSimilarities,useAggregateClustering)
    return output

# SUMMARIZE GIVEN DOCUMENT LIST  ACCORDING TO CLUSTERING AND RETURNS SUMMARY STRING
# PARAM: documents MULTIDOCUMENT LIST
# PARAM: aggregateSimilartyMatrix FLOAT MATRIX
# PARAM: length INTEGER
# PARAM: sentenceSimilarities TFIDF SENTENCE SIMILARITY
# PARAM: useAggregateClustering BOOLEAN USE COMBINED MATRIX AS SIMILARITY MATRIX OR NOT
def useClusteringAlgorithm(documents,aggregateSimilartyMatrix,length,sentenceSimilarities,useAggregateClustering):
    summarySet = selectSentences(length, aggregateSimilartyMatrix, sentenceSimilarities["idf_vectors"],
                                   documents,
                                   unit,
                                   None,
                                   'summarization_doc',
                                   use_aggregate_for_clustering=useAggregateClustering)

    summaryList = list(summarySet)
    summaryList.sort()
    returnString = ''
    for i in summaryList:
        returnString += ' '.join(getSentenceFromIndex(i, documents))+'\n'
    return returnString

# SUMMARIZE GIVEN DOCUMENT LIST  ACCORDING TO PAGERANK AND RETURNS SUMMARY STRING
# PARAM: documents MULTIDOCUMENT LIST
# PARAM: aggregateSimilartyMatrix FLOAT MATRIX
# PARAM: length INTEGER
# PARAM: alphaValueForPagerank FLOAT
# PARAM: alphaValueForMMR FLOAT
# PARAM: debugMode BOOLEAN
def usePageRankImplementation(documents,aggregateSimilartyMatrix,length,alphaValueForPagerank,alphaValueForMMR,debugMode):
    directedAndWeightedGraph = parseDirectedGraph(aggregateSimilartyMatrix)
    pageRankOutput =  rankMe(directedAndWeightedGraph,alphaValueForPagerank)
    ordererByIndexOutput = cutListByNumberOfWords(pageRankOutput,documents,aggregateSimilartyMatrix,length,debugMode,alphaValueForMMR)

    output = ""
    for innerText,text in ordererByIndexOutput:
        text = " ".join(text)
        output += text + " "

    return output.replace('`', '').replace('\'', '').replace('\n', '')
