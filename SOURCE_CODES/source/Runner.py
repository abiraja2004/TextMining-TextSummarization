from TextParser import *
from Manager import summarizeDocuments
from Util import  get_stopwords
import os ,itertools,csv
from evaluate import evaluate

DefaultStopwords   = os.path.split(os.path.realpath(__file__))[0] + '/config/english_stopwords.txt'
DefaultSummaryLength = 400
MinSentenceLength = 4

# MAIN FUNCTION d061j
# SUMMARIZE DOCUMENT WITH GIVEN PARAMETERS
# SUMMARIZATION RESULT USINGS ROUGE PACKAGE
def main():

    debugMode = True

    documentRoot = "../sumdata/data/d061j/"

    files = getSummaryFileList(documentRoot)
    orginalText = getStringsFromEE("../sumdata/extracts/d061ji/","400e")

    documents = parseText(documentRoot, files, MinSentenceLength, debugMode)
    stopwords = get_stopwords(DefaultStopwords)


    with open('results.csv', 'w') as csvfile:
        fieldnames = ['useWordModel', 'useTfIdfSimilarity', 'useSentimentSimilarity', 'usePageRank','useAggregateClustering','anaphoraResolution','ROUGE-1','ROUGE-2','ROUGE-3','ROUGE-SU4','ROUGE-L']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


        useWordModel = False
        useTfIdfSimilarity = True
        useSentimentSimilarity=True
        usePageRank = False
        useAggregateClustering = True
        anaphoraResolution = True

        alphaValueForPagerank = 0.85
        alphaValueForMMR = 0.999

        summary = summarizeDocuments(documents,
                                     stopwords,
                                     useTfIdfSimilarity,
                                     useSentimentSimilarity,
                                     useWordModel,
                                     usePageRank,
                                     useAggregateClustering,
                                     DefaultSummaryLength,
                                     anaphoraResolution,
                                     alphaValueForPagerank,
                                     alphaValueForMMR,
                                     debugMode)
        score = evaluate(orginalText, summary, debugMode)

        writer.writerow({
            'useWordModel': useWordModel,
            'useTfIdfSimilarity': useTfIdfSimilarity,
            'useSentimentSimilarity': useSentimentSimilarity,
            'usePageRank': usePageRank,
            'useAggregateClustering': useAggregateClustering,
            'anaphoraResolution': anaphoraResolution,
            'ROUGE-1' : score["ROUGE-1"],
            'ROUGE-2' : score["ROUGE-2"],
            'ROUGE-3' : score["ROUGE-3"],
            'ROUGE-SU4' : score["ROUGE-SU4"],
            'ROUGE-L' : score["ROUGE-L"]
        })
        csvfile.flush()
        print "\tROUGE-1:",score["ROUGE-1"],"\tROUGE-2:",score["ROUGE-2"], "\tROUGE-3:",score["ROUGE-3"],"\tROUGE-SU4:", score["ROUGE-SU4"],"\tROUGE-L:",score["ROUGE-L"]




if  __name__ =='__main__':main()
