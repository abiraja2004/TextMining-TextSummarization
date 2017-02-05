from operator import itemgetter

import  numpy

def analyzeSentiment(sentences,positiveWords,negativeWords,debugMode):
    emo_vectors = []
    for s in sentences:
        positive_count = 0
        negative_count = 0
        positive_frac = 0.0
        negative_frac = 0.0

        if len(s) > 0:
            for w in s:
                #"print w
                w = filter(str.isalnum, w)
                if w.lower() in positiveWords:
                    if(debugMode):
                        print "positive word found : "+w
                    positive_count += 1
                elif w.lower() in negativeWords:
                    if(debugMode):
                        print "negative word found : "+w
                    negative_count += 1
            positive_frac = float(positive_count) / float(len(s))
            negative_frac = float(negative_count) / float(len(s))
        emo_vec = [positive_frac, negative_frac]
        emo_vectors.append(emo_vec)

    positive_matrix = numpy.zeros((len(sentences), len(sentences)))
    negative_matrix = numpy.zeros((len(sentences), len(sentences)))

    min_simpos = 1.0
    max_simpos = 0.0
    min_simneg = 1.0
    max_simneg = 0.0

    for normalize in [1,0]:
        for i in range(len(emo_vectors)):
            for j in range(len(emo_vectors)):
                simpos = 1-abs(emo_vectors[i][0]-emo_vectors[j][0])
                simneg = 1-abs(emo_vectors[i][1]-emo_vectors[j][1])
                sim = simpos
                if normalize == 1:
                    if simpos > max_simpos:
                        max_simpos = simpos
                    if simpos < min_simpos:
                        min_simpos = simpos
                    if simneg > max_simneg:
                        max_simneg = simneg
                    if simneg < min_simneg:
                        min_simneg = simneg
                else:
                    normalized_simpos = 0.0
                    normalized_simneg = 0.0
                    if len(sentences[i]) > 0 and len(sentences[j]) > 1:
                        if max_simpos-min_simpos > 0.0:
                            normalized_simpos = (simpos-min_simpos)/(max_simpos-min_simpos)
                        if max_simneg-min_simneg > 0.0:
                            normalized_simneg = (simneg-min_simneg)/(max_simneg-min_simneg)

                    positive_matrix[i][j] = normalized_simpos
                    negative_matrix[i][j] = normalized_simneg

    return (positive_matrix, negative_matrix)




