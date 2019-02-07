import numpy as np
import networkx as nx
import math
import subprocess
from multiprocessing import Process
from networkx.algorithms.connectivity import build_auxiliary_node_connectivity
from networkx.algorithms.flow import build_residual_network
from networkx.algorithms.connectivity import local_node_connectivity


def Connectivity(overlap, graph, baseoutput):
    coverage = 30.0
    H = build_auxiliary_node_connectivity(graph)
    R = build_residual_network(H, 'capacity')
    with open(baseoutput + '-Connectivity','w') as output:
        for ov in overlap:
            connect = local_node_connectivity(graph, ov.read1, ov.read2, auxiliary=H, residual=R) / float(coverage)
            output.write(str(connect) + '\n')

def Centrality(overlap, graph, baseoutput):
    k = 10
    z = nx.edge_betweenness_centrality(graph, k)
    with open(baseoutput + '-Centrality','w') as output:
        for ov in overlap:
            edge = ov
            if edge in z:
                central = z[edge]
            else:
                reverse_edge = (ov[1], ov[0])
                central =  z[reverse_edge]
            output.write(str(central) + '\n')

def Degree(overlap, graph, baseoutput):
    with open(baseoutput + '-Degree','w') as output:
        for ov in overlap:
            edge = ov
            degree = graph.degree(edge[0]) + graph.degree(edge[1])
            output.write(str(degree) + '\n')

def ShortestPath(overlap, graph, baseoutput):
    with open(baseoutput + '-ShortestPath','w') as output:
        for ov in overlap:
            edge = ov
            graph.remove_edge(edge[0], edge[1])
            try:
                sp = nx.shortest_path_length(graph, edge[0], edge[1])
            except:
                sp = 100000000
            graph.add_edge(edge[0], edge[1])
            output.write(str(sp) + '\n')

def Fit_Node2Vec(output_filename):
    subprocess.call("python2 node2vec/src/main.py --input " + output_filename + "-graph-edge-list  --output " + output_filename + "-n2v.emd", shell=True)


def Set_Node2Vec_dic(output_filename):
    n2voutput = open(output_filename + "-n2v.emd", 'r')
    n2voutput = n2voutput.read()
    n2voutput = n2voutput.split('\n')
    header = n2voutput[0].split()
    node2vecdic = {}
    for i in range(1, len(n2voutput) - 1):
        n2voutputline = n2voutput[i].split()
        node2vecdic[n2voutputline[0]] = n2voutputline[1:]
    return node2vecdic

def Get_Node2Vec(overlap, baseoutput):
    Fit_Node2Vec(baseoutput)
    node2vecdic = Set_Node2Vec_dic(baseoutput)
    with open(baseoutput + '-Node2Vec', 'w') as output:
        for ov in overlap:
            edge = ov
            dim1 = np.asarray(node2vecdic.get(str(edge[0])))
            dim2 = np.asarray(node2vecdic.get(str(edge[1])))
            dim1 = dim1.astype(float)
            dim2 = dim2.astype(float)
            n2v = np.add(dim1, dim2) / 2.0
            for i, v in enumerate(n2v):
                if i == 0:
                    output.write(str(v))
                else:
                    output.write(',' + str(v))
            output.write('\n')

def SpringLayout(overlap, graph, baseoutput):
    layout = nx.spring_layout(graph, dim=5)
    with open(baseoutput + '-SL','w') as output:
        for ov in overlap:
            edge = ov
            v1 = layout.get(edge[0])
            v2 = layout.get(edge[1])
            distance = 0
            for z in range(1, 5):
                distance = distance + math.pow((v1[z] - v2[z]), 2)
            distance = math.sqrt(distance)
            SL = distance
            output.write(str(SL) + '\n')


def SpectralLayout(overlap, graph, baseoutput):
    layout = nx.spectral_layout(graph, dim=5)
    with open(baseoutput + '-SLL','w') as output:
        for ov in overlap:
            edge = ov
            v1 = layout.get(edge[0])
            v2 = layout.get(edge[1])
            distance = 0
            for z in range(1, 5):
                distance = distance + math.pow((v1[z] - v2[z]), 2)
            distance = math.sqrt(distance)
            SL = distance
            output.write(str(SL) + '\n')

def Extract_All_Features(overlap, graph, output):
    ProcessList = list()
    p = Process(target=Centrality, args=(overlap, graph, output,))
    p.start()
    ProcessList.append(p)
    p = Process(target=Degree, args=(overlap, graph, output,))
    p.start()
    ProcessList.append(p)
    p = Process(target=ShortestPath, args=(overlap, graph, output,))
    p.start()
    ProcessList.append(p)
    p = Process(target=Get_Node2Vec, args=(overlap, output,))
    p.start()
    ProcessList.append(p)
    p = Process(target=SpringLayout, args=(overlap, graph, output,))
    p.start()
    ProcessList.append(p)
    p = Process(target=SpectralLayout, args=(overlap, graph, output,))
    p.start()
    ProcessList.append(p)
    for p in ProcessList:
        p.join()
