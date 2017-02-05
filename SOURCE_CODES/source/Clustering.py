#!/usr/bin/python
# -*- coding: utf-8 -*-

import math, numpy, os.path, re, sys,time, scipy.cluster.vq, random
from subprocess import call




DEFAULT_STOPWORDS = 'english_stopwords.txt'

DEFAULT_VECTORS_FILE_PREFIX = '/tmp/submod_py_vectors.'

MAX_RETRIES = 10

# THIS METHOD RETURNS THE CLUSTER SIZES ACCORDING TO GIVEN SENTENCES NUMBER
# %20 PERCENT OF THE SENTENCE COUNT.
def getK(N):
  K = (int)(0.2 * N + 0.5)
  if K == 0: K = 1
  return K

def getClusteringBySim(similarities, K, docName = None, keep=False, debug_sentences=None):
  return clusterIteration(similarities, K, similarity_matrix=True, debug_sentences=debug_sentences)

def getClusteringByVec(sentenceVectors, K, matrixFileName = None, docName = None, keep=False, debug_sentences=None):
  return clusterIteration(sentenceVectors, K, similarity_matrix=False, debug_sentences=debug_sentences)

def clusterIteration(matrix, K, similarity_matrix=True, debug_sentences=None):
  num_sentences = matrix.shape[1]
  if similarity_matrix:
    similarities = matrix
  else:
    similarities = numpy.zeros((num_sentences, num_sentences))
    for i in xrange(0, num_sentences):
      for j in xrange(0, num_sentences):
        similarities[i][j] = numpy.dot(matrix[i], matrix[j])/numpy.sqrt(numpy.dot(matrix[i], matrix[i]))*numpy.sqrt(numpy.dot(matrix[j], matrix[j]))
  sentences = range(0,num_sentences)
  candidate_clustering = [0]*num_sentences
  candidate_medoids = [0]*K

  medoids = random.sample(sentences, K)

  cluster_members = assignToBestCluster(similarities, medoids)


  current_utility = clusterinUtil(similarities, medoids, cluster_members)
  prev_utility = -1

  iterations = 0
  while current_utility-prev_utility > 0:#prev_utility*.01:
    prev_utility = current_utility
    improving = False
    iterations += 1

    for c in xrange(0,len(medoids)):
      medoids[c] = getBestMedoid(similarities, cluster_members[c])
    cluster_members = assignToBestCluster(similarities, medoids)
    current_utility = clusterinUtil(similarities, medoids, cluster_members)

  clustering = [0]*num_sentences
  for c in xrange(0,len(cluster_members)):
    for s in cluster_members[c]:
      clustering[s] = c
  if debug_sentences:
    print "Outputting clustering. Below (all zero-based): medoid, sentence1 (medoid_distance), sentence2 (medoid_distance), ..."
    for m in medoids:
      c = medoids.index(m)
      members = list(cluster_members[c])
      simlist = list()
      print "\"***cluster of size %d. medoid: %s\""%(len(members),' '.join(debug_sentences[m])),
      for s in members:
        simlist.append((s,similarities[m][s]))
      backwards = [(v[1],v[0]) for v in simlist]
      backwards.sort(reverse=True)
      forwards = [(v[1],v[0]) for v in backwards]
      for pair in forwards:
        print "\"%s\""%' '.join(debug_sentences[pair[0]]),
        print "(%.3f)"%pair[1],
      print "\n"
    
  return clustering

def assignToBestCluster(similarities, medoids):
  num_sentences = similarities.shape[0]
  cluster_members = list()
  for c in xrange(0,len(medoids)):
    cluster_members.append(set())
  for s in xrange(0,num_sentences):
    if s in medoids:
      c = medoids.index(s)
      cluster_members[c].add(s)
    else:
      c_best = 0
      max_sim = 0.0
      for c in xrange(0,len(medoids)):
        m = medoids[c]
        #print "medoid: %d, max_sim: %f, sim: %f"%(m, max_sim, similarities[s][m])
        if similarities[s][m] > max_sim:
          max_sim = similarities[s][m]
          c_best = c
      cluster_members[c_best].add(s)
  return cluster_members

def getBestMedoid(similarities, cluster_members):
  if len(cluster_members) == 1:
    for candidate in cluster_members:
      return candidate
  best_medoid = -1
  best_medoid_sim = -1
  for candidate in cluster_members:
    candidate_sim = 0.0
    for s in cluster_members:
      if candidate == s:
        continue
      candidate_sim += similarities[candidate][s]
    if candidate_sim > best_medoid_sim:
      best_medoid_sim = candidate_sim
      best_medoid = candidate
  return best_medoid

def clusterinUtil(similarities, medoids, cluster_members):
  cluster_utility = 0.0
  for c in xrange(0,len(medoids)):
    medoid = medoids[c]
    for s in cluster_members[c]:
      cluster_utility += similarities[medoid][s]
  return cluster_utility

