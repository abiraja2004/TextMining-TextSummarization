from TfIdfCalculator import getTfIdfValues
from Clustering import getClusteringBySim
from Clustering import getK
from Util import  get_stopwords
import  os
DEFAULT_STOPWORDS   = os.path.split(os.path.realpath(__file__))[0]+'/english_stopwords.txt'

def get_clustering( aggregateSimilarityMatrix):

    K = getK(aggregateSimilarityMatrix.shape[0])
    clustering = getClusteringBySim(aggregateSimilarityMatrix, K, "summarization_doc")#, debug_sentences=flat_sentences)
    return clustering