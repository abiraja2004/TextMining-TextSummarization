import networkx as nx

# THIS METHOD RETURNS DIRECTED GRAPH OF GIVEN DATA
def parseDirectedGraph(data):
    DG = nx.DiGraph()
    nodes = list()
    for i in range(0,len(data)):
        nodes.append(i)

    rank = 1/float(len(data))
    DG.add_nodes_from(nodes, rank=rank)

    for i, row in enumerate(data):
        for j, column in enumerate(row):
            column = float(column)
            if column > 0.005:
                DG.add_edge(i,j,weight = column)

    return DG