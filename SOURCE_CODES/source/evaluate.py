import sys
sys.path.insert(0, '../evaluation/python/pythonrouge/')
from pythonrouge import *

# THIS METHOD RETURNS SCORE OF ROUGE EVAULATION WITH GIVEN SENTENCES
def evaluate(orginalText,textToCompare,debugMode):

    if(debugMode):
        print("ORGINAL TEXT: ", orginalText)
        print("TEXT TO COMPARE: ", textToCompare)

    ROUGE_path = "../evaluation/ROUGE-1.5.5.pl"
    data_path = "../evaluation/data"

    score = pythonrouge(orginalText, textToCompare,ROUGE_path,data_path)
    return score
#debug purpose
#scoree = evaluate("it is a CAR","it is a car", True)
#print (scoree)

