import FeatureExtractor
import sys
import re
import networkx as nx
import UseExistingClassifier
import FilterOverlaps

def Overlap_From_Paf(paf_filepath):
    overlap_list = list()
    with open(paf_filepath) as paf:
        for line in paf:
            line = line[:-1].split()
            read1 = int(re.search(r'\d+', line[0]).group())
            read2 = int(re.search(r'\d+', line[5]).group())
            if read1 >= read2:
                continue
            else:
                overlap = (read1, read2)
                overlap_list.append(overlap)
    return overlap_list

if __name__ == '__main__':
    paf_filepath = "/home/ramin/PycharmProjects/tudelft/2018/data/yeast/s.cerevisiae.fasta-chr-BK006938.2-ploidy1-cov-30-1531933-9/overlaps.paf"
    output = 'results/temp'
    overlap_list = Overlap_From_Paf(paf_filepath)
    graph = nx.Graph(overlap_list)
    nx.write_edgelist(graph, output + '-graph-edge-list')
    #FeatureExtractor.Extract_All_Features(overlap_list, graph, output)
    classification_results = UseExistingClassifier.classifyoverlaps(output, 'models/model-potato-c0.01', 0.1)
    FilterOverlaps.filter(paf_filepath, overlap_list, classification_results, output)
    print("Done")