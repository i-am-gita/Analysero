import networkx as nx
import random as rnd

'''
    Metoda koja ucitava bitcoin alpha mrezu sa Stanforda i pretvara je u neusmerenu.
'''
def loadBitcoin(path):
    G = nx.DiGraph()
    import csv
    with open(path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if int(row[2]) > 0:
                afn = "1"
            else:
                afn = "-1"
            G.add_edge(row[0], row[1], affinity=afn)
    csv_file.close()
    return fromDirectedToUndirected(G)


'''
    Metoda koja od usmerenog grafa pravi neusmereni graf i vraca ga kao return vrednost.
    Radi tako sto iterira kroz cvorove grana i proverava afinitete (ukoliko je bar u jednom smeru bio minus, minus ostaje i u neusmerenom grafu).
    U suprotnom se stavlja plus.
'''
def fromDirectedToUndirected(directedGraph):
    undirectedGraph = nx.Graph()
    undirectedGraph.add_edges_from(directedGraph.edges(), affinity="")
    for u, v, d in directedGraph.edges(data=True):
        afn1 = directedGraph[u][v]['affinity']
        afn2 = ""
        if (v, u) in directedGraph.edges:
            afn2 = directedGraph[v][u]['affinity']
        if afn1 == "-1" or afn2 == "-1":
            undirectedGraph[u][v]['affinity'] = "-1"
        else:
            undirectedGraph[u][v]['affinity'] = "1"

    return undirectedGraph


'''
    Metoda koja ucitava usmerenu Epinions mrezu  i Slashdot usmerenu mrezu, te ih vraca kao neusmerene.
'''
def loadEpinionsAndSlashNetworks(fileName):
    file = open(fileName,"r")
    graph=nx.DiGraph()
    for line in file:
        if line.startswith("#")==False:
            row = line.split()
            if row[0].strip() not in graph.nodes:
                graph.add_node(row[0])
            if row[1].strip() not in graph.nodes:
                graph.add_node(row[1])
            graph.add_edge(row[0],row[1],affinity=row[2].strip())
    return fromDirectedToUndirected(graph)


def loadWikiNetwork():
    file = open("wiki-RfA.txt","r", encoding="utf8")
    graph=nx.DiGraph()
    for line in file:
        if line.startswith("SRC"):
            source=line.split(":")[1]
            if source not in graph.nodes:
                graph.add_node(source)

        if line.startswith("TGT"):
            target=line.split(":")[1]
            if target not in graph.nodes:
                graph.add_node(target)

        if line.startswith("RES"):
            res=line.split(":")[1].strip()
            if res=="+1":
                res="1"
            elif res=="-1":
                res="-1"
            graph.add_edge(source,target,affinity=res)
    i = 0
    k=0
    for node1, node2, data in graph.edges(data=True):
        if data['affinity']=="-1":
            i=i+1
        if data['affinity']=="1":
            k=k+1
    print(i,"negativ")
    print(k,"possitiv")
    return fromDirectedToUndirected(graph)
#Prvo se pravi numNodes čvorova i svakom čvoru se dodeljuje atribut "cluster" koji određuje kojem će klasteru pripadati
# (postoji jednaka verovatnoća za pripadanje svim klasterima). Nakon ovoga se prolazi kroz svaki par čvorova kod kojih postoji
# 50 posto šanse da se ta dva čvora spoje granom. Ukoliko su ti čvorovi iz istog klastera(isti atribut cluster) onda se spajaju
#pozitivnom granom, u suprotnom se spajaju negativnom granom
def makeCustomClusterableGraph():
    print("How many nodes would you like your graph to have?")
    numNodes = input("->")
    graph=nx.Graph()
    numClusters = rnd.randint(1,int(numNodes))
    for i in range(int(numNodes)):
        clusterChoice=rnd.randint(1,numClusters)
        graph.add_node(i,cluster=clusterChoice)

    for node in graph.nodes:
        for otherNode in graph.nodes:
            if node == otherNode:
                continue
            chance = rnd.randint(1,50)
            if chance == 1:
                if not (graph.has_edge(node,otherNode) or graph.has_edge(otherNode, node)):
                    if graph.node[node]['cluster'] == graph.node[otherNode]['cluster']:
                        graph.add_edge(node,otherNode,affinity='+1')
                    else:
                        graph.add_edge(node,otherNode,affinity='-1')
    return graph
