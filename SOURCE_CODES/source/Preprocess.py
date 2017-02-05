import  os.path, sys

#ANAPHORA RESOLUTION
def preprocess(documents, femaleNamesFileName, maleNamesFileName, anaphoraResolution, debugMode):
  femaleNames = readFile(femaleNamesFileName)
  maleNames = readFile(maleNamesFileName)

  if anaphoraResolution:
    documents_to_return = list()
    try:
      for document in documents:
        documentToReturn = list()
        previousPersonMale = None
        previousPersonFemale = None
        for sentence in document:
          newPersonMale = None
          newPersonFemale = None
          skip = False
          for i in range(0, len(sentence)):
            if skip:
              skip = False
              continue
            word = filter(str.isalnum, sentence[i])
            if word in maleNames:
              if (debugMode):
                print "male name %s"%word
              newPersonMale = [word]
              if len(sentence) > i+1:
                next_word = filter(str.isalnum, sentence[i+1])
                if next_word.istitle():
                  newPersonMale.append(next_word)
                  skip = True
            if word in femaleNames:
              if (debugMode):
                print "female name %s"%word
              newPersonFemale = [word]
              if len(sentence) > i+1:
                next_word = filter(str.isalnum, sentence[i+1])
                if next_word.istitle():
                  newPersonFemale.append(next_word)
                  skip = True
          processed_sentence = list()
          for i in xrange(0, len(sentence)):
            if isPronounToReplace(sentence[i]):
              if(debugMode):
                print " ".join(sentence)
                print "is pronoun to replace %s"%sentence[i]
              possessive_suffix = ""
              if isPossessivePronoun(sentence[i]):
                possessive_suffix = "'s"
              punctuation = ""
              last_char = sentence[i][-1]
              word_without_punctuation = sentence[i]
              if isPunctuation(last_char):
                punctuation = last_char
                word_without_punctuation = sentence[i][:-1]
              if isMalePronoun(sentence[i]) and (newPersonMale is not None):
                if(debugMode):
                    print "%s is male pronoun! new person male is not none. %s."%(possessive_suffix, str(previousPersonMale))
                processed_sentence.append(sentence[i])
              elif isMalePronoun(sentence[i]) and (previousPersonMale is not None):
                if(debugMode):
                    print "%s is male pronoun! %s."%(possessive_suffix, str(previousPersonMale))
                processed_sentence.append(word_without_punctuation)
                list_to_append = copy.deepcopy(previousPersonMale)
                list_to_append[0] = "("+list_to_append[0]
                list_to_append[-1] = list_to_append[-1]+possessive_suffix+")"+punctuation
                for term in previousPersonMale:
                  processed_sentence.append(term)
              elif isFemalePronoun(sentence[i]) and (newPersonFemale is not None):
                processed_sentence.append(sentence[i])
              elif isFemalePronoun(sentence[i]) and (previousPersonFemale is not None):
                processed_sentence.append(word_without_punctuation)
                list_to_append = copy.deepcopy(previousPersonFemale)
                list_to_append[0] = "("+list_to_append[0]
                list_to_append[-1] = list_to_append[-1]+possessive_suffix+")"+punctuation
                for term in previousPersonMale:
                  processed_sentence.append(term)
              else:
                processed_sentence.append(sentence[i])
            else:
              processed_sentence.append(sentence[i])
          if processed_sentence != sentence and not quiet:
            print "preprocessed: %s"%(' '.join(processed_sentence))
          documentToReturn.append(processed_sentence)
          if newPersonMale is not None:
            previousPersonMale = newPersonMale
          if newPersonFemale is not None:
            previousPersonFemale = newPersonFemale
        documents_to_return.append(documentToReturn)
    except Exception, e:
      print e
      return documents
    return documents_to_return
  else:
    return documents

def readFile(filename):
  wordlist = list()
  f = open(os.path.abspath(os.path.dirname(sys.argv[0]))+'/'+filename, 'r')
  for line in f:
    stripped = line.strip()
    if stripped:
      wordlist.append(stripped)
  f.close()
  return wordlist

def isPunctuation(char):
  return char in [".", "?", ",", "!", ")"]

def isPluralPronoun(word):
  if len(word) > 0 and isPunctuation(word[-1]):
    word = word[:-1]
  return word.lower() in ["they", "their", "we", "our", "we're", "they're"]

def isPossessivePronoun(word):
  if len(word) > 0 and isPunctuation(word[-1]):
    word = word[:-1]
  return word.lower() in ["his", "her", "its", "their"]

def isPronounToReplace(word):
  if len(word) > 0 and isPunctuation(word[-1]):
    word = word[:-1]
  return word.lower() in ["he", "his", "she", "her", "s/he", "they", "their", "they're"]
  
def isMalePronoun(word):
  if len(word) > 0 and isPunctuation(word[-1]):
    word = word[:-1]
  return word.lower() in ["he", "his", "s/he"]

def isFemalePronoun(word):
  if len(word) > 0 and isPunctuation(word[-1]):
    word = word[:-1]
  return word.lower() in ["she", "her", "s/he"]