import os
import xml.etree.ElementTree

def getStringsFromEE(documentRoot,document_name):
    root = xml.etree.ElementTree.parse(documentRoot+document_name).getroot()
    chunks = []
    for child in root:
        chunks.append(child.text.replace('\n', ''))
    return '\n'.join(chunks)

def getSummaryFileList(documentRoot):
    allDocumentsList = list()
    dataSubdirectories = os.listdir(documentRoot)
    for dataDirectory in dataSubdirectories:
        if(len(dataDirectory)>10):
            allDocumentsList.append(dataDirectory)
    return allDocumentsList


def parseText(documentRoot,document_names,min_sentence_length,debugMode):
    allLinesList = list()
    totalNumberOfLines = 0
    for filename in document_names:
        root = xml.etree.ElementTree.parse(documentRoot+filename).getroot()
        lines = list()
        for child in root:
            if (child.tag=="TEXT"):
                for children in child:
                    lines.append(children.text.strip())
        lineCountInSingleFile = len(lines);
        totalNumberOfLines+= lineCountInSingleFile
        if(debugMode):
            print "\tline count in ",filename," : ",lineCountInSingleFile
        allLinesList.append(lines)
    if(debugMode):
        print "Total line count in all files : ",totalNumberOfLines

    sentence_count = 0
    documents = []

    for l in allLinesList:
        document = list()
        for s in l:
            stripped = s.strip()
            wordlist = stripped.split()
            if len(wordlist) >= min_sentence_length:
                sentence_count += 1
                document.append(wordlist)
        documents.append(document)

    return documents





