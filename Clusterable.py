import networkx as nx

def components(graph):
    visited=set()
    components=set()
    for node in graph.nodes:
        if node not in visited:
            components.add(bfs(node,visited,graph))
    print(f"Graph is made out of  {len(list(components))} clusters")
    return frozenset(components)

def bfs(node,visited,graph):
    compSet=set()
    queue=list()
    compSet.add(node)
    visited.add(node)
    queue.append(node)
    while not len(queue)==0:
        current=queue.pop(0)
        neighbours = list(nx.neighbors(graph,current))
        for neighbour in neighbours[:]:
            afn1 = graph.get_edge_data(current,neighbour)
            afn2 = graph.get_edge_data(neighbour, current)
            if afn1['affinity'] == "-1" or afn2['affinity'] == "-1":
                neighbours.remove(neighbour)
        for neighbour in neighbours:
            if neighbour not in visited:
                compSet.add(neighbour)
                visited.add(neighbour)
                queue.append(neighbour)
    return frozenset(compSet)

def clusterGraphMaker(clusterSet, graph):
    clusters=set()
    print("Do you want to print number of nodes and edges for every clusterGraph? Y/N")
    choice = input("-> ")
    cnt=0
    for cluster in clusterSet:
        tmp = set([node for node in cluster])
        clusterGraph = graph.copy()
        for vertex in list(clusterGraph.nodes)[:]:
            if vertex not in tmp:
                clusterGraph.remove_node(vertex)
        clusters.add(clusterGraph)
        cnt=cnt+1
        if choice is "Y" or choice is "y":
            print("Cluster number ",cnt," has ",len(list(clusterGraph.nodes))," nodes and ",len(list(clusterGraph.edges))," edges")
    return clusters

''' Metoda koja u listi klastera koji su predstavljeni kao grafovi sami za sebe(podrmreze) nalazi onaj koji je bio predstavljen listom cvorova.
    Koristi se prilikom analize koalicija i antikoalicija'''
def findClusterGraph(clusterGraphs,clusterNodes):
    for clusterGraph in clusterGraphs:
        if clusterGraph.nodes == clusterNodes:
            return clusterGraph

def isClusterable(clusters):
    coalitions = list()
    antiCoalitions = list()
    badLinks = list()
    listOfCoalitionsAndAntiCoalitions = list()
    for cluster in clusters:
        clusterKiller= [(u,v) for (u,v,d) in cluster.edges(data=True) if d['affinity'] == "-1"]
        if len(clusterKiller) == 0:
            coalitions.append(cluster.nodes)
        else:
            antiCoalitions.append(cluster.nodes)
            badLinks.extend(clusterKiller)

    if len(antiCoalitions) == 0:
        print("Given graph is clusterable because there are no anti-coalitions")
    else:
        print("Given graph is not clusterable because of existing anti-coalitons."
              "Do you want to see links that should be deleted in order for this graph to become clusterable? Y/N")
        choice = input("-> ")
        if choice is "y" or "Y":
            for link in badLinks:
                print(link)

    listOfCoalitionsAndAntiCoalitions.append(coalitions)
    listOfCoalitionsAndAntiCoalitions.append(antiCoalitions)

    return listOfCoalitionsAndAntiCoalitions

'''
    Clusteri su predstavljeni kao skup skupova cvorova, a ne kao grafovi.
    Metoda radi tako sto prolazi kroz sve kombinacije cvorova iz razlicitih klastera i proverava da li su susedi u prvobitnom grafu.
    Ukoliko jesu susedi, on pravi cvorove u novom grafu networks(ukoliko vec ne postoje) i povezuje ih linkom
'''
def clusterNetworkMaker(clusters,graph):
    network=nx.Graph()
    for cluster in clusters:
        for otherCluster in clusters:
            if cluster == otherCluster:
                continue
            connected = False
            for node in cluster:
                for otherNode in otherCluster:
                    if node in graph.neighbors(otherNode):
                        network.add_node(str(cluster))
                        if str(cluster) not in network.nodes:
                            network.add_node(str(cluster))
                        if str(otherCluster) not in network.nodes:
                            network.add_node(str(otherCluster))
                        network.add_edge(str(cluster),str(otherCluster))
                        connected = True
                        break
                if connected == True:
                    break
    return network

def getNeighbours(current,graph):
    neighbours=[]
    affinity = nx.get_edge_attributes(graph,'affinity')
    for edge in graph.edges():
        if affinity[edge]==1:
            if edge[0]==current:
                neighbours.append(edge[1])
            elif edge[1]==current:
                neighbours.append(edge[0])
    return neighbours



