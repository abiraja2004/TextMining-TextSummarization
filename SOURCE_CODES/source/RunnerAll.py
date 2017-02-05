from TextParser import *
from Manager import summarizeDocuments
from Util import  get_stopwords
import os ,itertools,csv
from evaluate import evaluate
from datetime import datetime

DefaultStopwords   = os.path.split(os.path.realpath(__file__))[0] + '/config/english_stopwords.txt'
DefaultSummaryLength = 400
MinSentenceLength = 4

def main():

    debugMode = False
    stopwords = get_stopwords(DefaultStopwords)

    with open('results.csv', 'w') as csvfile:
        fieldnames = ['time','file','useWordModel', 'useTfIdfSimilarity', 'useSentimentSimilarity', 'usePageRank','useAggregateClustering','anaphoraResolution','ROUGE-1','ROUGE-2','ROUGE-3','ROUGE-SU4','ROUGE-L']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        a = [True, False]
        dataDirectoryRoot = "../sumdata/data/"
        extractDirectoryRoot = "../sumdata/extracts/"
        dataSubdirectories = os.listdir(dataDirectoryRoot)
        dataSubdirectories = sorted(dataSubdirectories)
        evaluationSubdirectories = os.listdir(extractDirectoryRoot)

        for i in itertools.product(a,a,a,a,a,a):
            useWordModel = i[0]
            useTfIdfSimilarity = i[1]
            useSentimentSimilarity=i[2]
            usePageRank = i[3]
            useAggregateClustering = i[4]
            anaphoraResolution = i[5]

            alphaValueForPagerank = 0.85
            alphaValueForMMR = 0.999

            print "========================================================================================================"

            numberOfIter = 0

            totalNumberOfItems = 0
            avaragerougeOneScore = 0
            avaragerougeTwoScore = 0
            avaragerougeThreeScore = 0
            avaragerougeSU4Score = 0
            avaragerougeLScore = 0

            filesNames = []
            for dataDirectory in dataSubdirectories:
                for extractDirectory in evaluationSubdirectories:
                    if extractDirectory.__contains__(dataDirectory):
                        numberOfIter = numberOfIter+1
                        if(numberOfIter in [3,4,9,10,11,12]):
                            continue
                        if(numberOfIter>15):
                            break
                        print "--------------------------------------------------------------------------------------------------------"
                        print "\t\t\t\t\t\t\t\t",dataDirectory+ " - "+extractDirectory,numberOfIter
                        try:
                            files = getSummaryFileList(dataDirectoryRoot+dataDirectory+"/")
                            orginalText = getStringsFromEE(extractDirectoryRoot+extractDirectory,"/400e")
                            documents = parseText(dataDirectoryRoot+dataDirectory+"/", files, MinSentenceLength, debugMode)

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

                            totalNumberOfItems = totalNumberOfItems +1
                            avaragerougeOneScore += score["ROUGE-1"]
                            avaragerougeTwoScore += score["ROUGE-2"]
                            avaragerougeThreeScore += score["ROUGE-3"]
                            avaragerougeSU4Score  += score["ROUGE-SU4"]
                            avaragerougeLScore  += score["ROUGE-L"]
                            filesNames.append(dataDirectory)
                            print i
                        except Exception as e:
                            print e

            writer.writerow({
                'time':str(datetime.now()),
                'file':"-".join(filesNames),
                'useWordModel': useWordModel,
                'useTfIdfSimilarity': useTfIdfSimilarity,
                'useSentimentSimilarity': useSentimentSimilarity,
                'usePageRank': usePageRank,
                'useAggregateClustering': useAggregateClustering,
                'anaphoraResolution': anaphoraResolution,
                'ROUGE-1' : "%.4f" % ( avaragerougeOneScore/totalNumberOfItems),
                'ROUGE-2' : "%.4f" %(avaragerougeTwoScore/totalNumberOfItems),
                'ROUGE-3' : "%.4f" %(avaragerougeThreeScore/totalNumberOfItems),
                'ROUGE-SU4' : "%.4f" %(avaragerougeSU4Score/totalNumberOfItems),
                'ROUGE-L' : "%.4f" %(avaragerougeLScore/totalNumberOfItems)
            })
            csvfile.flush()


if  __name__ =='__main__':main()