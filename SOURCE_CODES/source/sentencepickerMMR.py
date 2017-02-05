import operator,re


def cutListByNumberOfWords(pageRankOutput,sentencesList,similarityData,numberOfWords,debugMode, lambdaValue = 0.95):

    allSentenceList = list()
    for element in sentencesList:
        allSentenceList.extend(element)

    totalNumberOfLines=0
    output =[]
    sortedRelevence = sorted(pageRankOutput.iteritems(), key=operator.itemgetter(1), reverse=True)
    while (True):
        if(debugMode):
            print  "sortedRelevence : ",sortedRelevence
        highestValue = sortedRelevence[0]
        highestRankedSentence = [highestValue[0],allSentenceList[highestValue[0]]]
        count = len(highestRankedSentence[1])
        totalNumberOfLines = totalNumberOfLines + count
        if (totalNumberOfLines<numberOfWords):
            output.append(highestRankedSentence)
            del sortedRelevence[0]
            for idx, row in enumerate(sortedRelevence):
                id, name = row
                sortedRelevence[idx] = (id, (lambdaValue*name)-((1-lambdaValue)*float(similarityData[highestValue[0]][id])))
            sortedRelevence = sorted(sortedRelevence, key=operator.itemgetter(1),reverse=True)
        else:
            break

    ordererByIndexOutput = sorted(output, key=operator.itemgetter(0))
    return ordererByIndexOutput