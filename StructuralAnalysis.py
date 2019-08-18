import networkx as nx

def clusterScore(clusterGraph,score):
    avgDg = averageDegree(clusterGraph)
    score['avgDg'].append(avgDg)
    avgDst = averageDistance(clusterGraph)
    score['avgDg'].append(avgDst)
    netDens = networkDensity(clusterGraph)
    score['netDens'].append(netDens)
    netDia = networkDiameter(clusterGraph)
    score['netDia'].append(netDia)
    return score
def averageDegree(graph):
    return 2*graph.number_of_edges() / float(graph.number_of_nodes())

'''
def clusterDegreeSequence(graph,cluster):
    nodeDeg = list()
    for node in cluster:
        nodeDeg.append(graph.degree[node])
    degSeq = [degree for node, degree in nodeDeg]
    print("Degree histogram: ")
    histogram = {}
    for degree in nodeDeg:
        if degree in histogram:
            histogram[degree] +=1
        else:
            histogram[degree] = 1
    for degree in histogram:
        print('%d %d' %(degree, histogram[degree]))
'''

def networkDegreeSequence(graph):
    degSeq = [degree for node, degree in graph.degree()]
    print("Degree histogram: ")
    histogram = {}
    for degree in degSeq:
        if degree in histogram:
            histogram[degree] += 1
        else:
            histogram[degree] = 1
    for degree in histogram:
        print('%d %d' %(degree, histogram[degree]))
def averageDistance(cluster):
    return nx.average_shortest_path_length(cluster)

def networkDensity(network)
    numOfNodes = network.number_of_nodes()
    numOfEdges = network.number_of_edges()
    density = (2*numOfEdges)/(numOfNodes*(numOfNodes-1))
    return density

def networkDiameter(network):
    return nx.diameter(network)

def isCommunityAndCutMetrics(network,cluster):
    edgeCuts = 0
    radiciStrong = True
    for node in cluster.nodes:
        interDegreeNeighbors = 0
        for n in nx.neighbors(network,node):
            if not cluster.has_edge(node,n): #Da li treba i (n, node)?
                edgeCuts +=1
                interDegreeNeighbors += 1
        if len(nx.neighbors(cluster,node)) < interDegreeNeighbors:
            radiciStrong = False
    intraLinks = cluster.number_of_edges()

    conductance = edgeCuts / (edgeCuts + intraLinks)
    expansion = edgeCuts / cluster.number_of_nodes
    cutRatio = edgeCuts / (cluster.number_of_nodes*(network.number_of_nodes - cluster.number_of_nodes))

    print("Cut metrics for this cluster: ")
    print("Conductance: ",conductance)
    print("Expansion: ", expansion)
    print("Cut-ratio: ",cutRatio)

    p = (2*intraLinks) / (cluster.number_of_nodes*(cluster.number_of_nodes - 1))
    q = edgeCuts / (cluster.number_of_nodes*(network.number_of_nodes - cluster.number_of_nodes))
    if p>(q*5):
        if radiciStrong:
            print("This cluster represent Radici strong community")
        else:
            if intraLinks > edgeCuts:
                print("This cluster represent radici weak community")
            else:
                print("This cluster is community")
    else:
        print("This cluster is not community")
