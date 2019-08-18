import networkx as nx
from LoadNetworks import loadEpinionsAndSlashNetworks
from LoadNetworks import loadBitcoin
from LoadNetworks import makeCustomClusterableGraph
from Clusterable import clusterGraphMaker
from Clusterable import isClusterable
from Clusterable import clusterNetworkMaker
from LoadNetworks import loadWikiNetwork
from Clusterable import components
from Clusterable import findClusterGraph
from StructuralAnalysis import clusterScore
def main():

    network = pickGraph()
    print("Network is made out of ", len(network.nodes)," nodes, and ", len(network.edges)," edges.")
    clusterGraphs = clusterGraphMaker(components(network),network)
    coalitionsAndAnticoalitions=isClusterable(clusterGraphs)
    print("There are ",len(coalitionsAndAnticoalitions[0])," coalitions and ",len(coalitionsAndAnticoalitions[1]), "anticoalitions:")
    print("---------------------------------------------------------")
    print("Coalitions:")
    for coalition in coalitionsAndAnticoalitions[0]:
        print(coalition)
    print("---------------------------------------------------------")
    print("Anticoalitions:")
    for anti in coalitionsAndAnticoalitions[1]:
        print(anti)
    print("---------------------------------------------------------")
    score = {'avgDg': [], 'avgDst': [], 'netDens':[],'netDia':[]}
    for coalition in coalitionsAndAnticoalitions[0]:
        coGraph = findClusterGraph(clusterGraphs, coalition)
        score = clusterScore(coGraph,score)

    score2 = {'avgDg': [], 'avgDst': [], 'netDens':[],'netDia':[]}
    for antiCo in coalitionsAndAnticoalitions[1]:
        coGraph = findClusterGraph(clusterGraphs,antiCo)
        score2 = clusterScore(coGraph,score2)

    if sum(score['avgDg']) > sum(score2['avgDg']):
        print("Coalitions are more cohesive then the anticoalitions")
    else:
        print("Anticoalitions are more cohesive then the coalitions")









    clusterNet = clusterNetworkMaker(components(network),network)
    print("Network of clusters is made out of ", len(clusterNet.nodes)," nodes, and ",len(clusterNet.edges)," edges.")

def pickGraph():
    print("Choose what network would you like to load:")
    print("1 - Epinions Network")
    print("2 - Wikipedia Network")
    print("3 - SlashDot Network")
    print("4 - Bitcoin Network")
    print("5 - Generate random network with custom number of vertices and clusters")
    while True:
        choice = input("->")
        if choice == "1":
            return loadEpinionsAndSlashNetworks("soc-sign-epinions.txt")
        elif choice == "2":
            return loadWikiNetwork()
        elif choice == "3":
            return loadEpinionsAndSlashNetworks("soc-sign-Slashdot081106.txt")
        elif choice == "4":
            return loadBitcoin("soc-sign-bitcoinalpha.csv")
        elif choice == "5":
            return makeCustomClusterableGraph()





if __name__ == '__main__':
    main()
