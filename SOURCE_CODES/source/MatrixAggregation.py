import math, numpy

def calcAggregateSimMatrix(ms):
    if len(ms) == 1:
        return ms[0]

    aggregateSim = numpy.array(ms[0], copy=True)

    for k in range(1,len(ms)):
        m = ms[k]
        for i in range(0, m.shape[0]):
            for j in range(0, m.shape[1]):
                aggregateSim[i][j] = (aggregateSim[i][j] - m[i][j])**2

    minval = 1.0
    maxval = 0.0
    for i in range(0, aggregateSim.shape[0]):
        for j in range(0, aggregateSim.shape[1]):
            if aggregateSim[i][j] < minval:
                minval = aggregateSim[i][j]
            if aggregateSim[i][j] > maxval:
                maxval = aggregateSim[i][j]

    aggregateSim = (aggregateSim-minval)/(maxval-minval)
    return aggregateSim

def L1(S, w, alpha, a):
    if not alpha:
        alpha = a/(1.0*w.shape[0])
    res = 0.0
    for i in range(0, w.shape[0]):
        sum_val = 0.0; sumV = 0.0
        for j in S:
            sum_val += w[i][j]
        for k in range(0,w.shape[0]):
            sumV += w[i][k]
        sumV *= alpha
        res += min(sum_val, sumV)
    return res

def R1(S, w, clustering, K):
    N = w.shape[0]
    res = 0.0
    for k in range(0, K):
        sum_val = 0.0
        for j in S:
            if (clustering [j] == k):
                sumV = 0.0
                for i in range(0,N):
                    sumV += w [i][j]
                sum_val += sumV / N
        res += math.sqrt(sum_val)
    return res

def normalize(m):
    max_v = 0.0
    mr = zeroes((m.shape[0],m.shape[1]))
    #Get the  max_v:
    for i in range(0, m.shape[0]):
        for j in range(0, m.shape[1]):
            if m[i][j] > max_v:
                max_v = m[i][j]

    #Normalize:
    for i in range(0, m.shape[0]):
        for j in range(0, m.shape[1]):
            mr[i][j] = m[i][j]/max_v
    return mr






