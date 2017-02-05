def rankMe(graph, alpha=0.85 , numberOfIterations=100, treshold=1.0e-6):

    weight='weight'
    degree = graph.out_degree(weight=weight)
    for (uu, vv, dd) in graph.edges(data=True):
        if degree[uu] == 0:
            print 'zero out-degree for node',uu
            dd[weight] = 0
        else:
            dd[weight] = dd.get(weight, 1) / degree[uu]

    numberOfNodes = graph.number_of_nodes()

    x = dict.fromkeys(graph, 1.0 / numberOfNodes)
    p = dict.fromkeys(graph, 1.0 / numberOfNodes)
    dangling_weights = p
    dangling_nodes = [n for n in graph if graph.out_degree(n, weight='weight') == 0.0]

    # loop numberOfIterations times
    for _ in range(numberOfIterations):
        xlast = x
        x = dict.fromkeys(xlast.keys(), 0)
        danglesum = alpha * sum(xlast[n] for n in dangling_nodes)
        for n in x:
            for nbr in graph[n]:
                x[nbr] += alpha * xlast[n] * graph[n][nbr]['weight']
            x[n] += danglesum * dangling_weights[n] + (1.0 - alpha) * p[n]
        err = sum([abs(x[n] - xlast[n]) for n in x])
        if err < numberOfNodes*treshold:
            return x
    print "hata"


