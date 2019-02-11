import FeatureExtractor
import re
import networkx as nx
import UseExistingClassifier
import FilterOverlaps
import argparse


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
    parser = argparse.ArgumentParser("GraphClean detect remove induced overlaps in a paf file and remove them")
    parser.add_argument("PAF", help="Path to the input PAF file which contains overlaps")
    parser.add_argument("Output", help="Output files prefix")
    parser.add_argument("-m", "--model", help="Path to the model, models are inside models directory", default= "models/model-potato-c0.1")
    parser.add_argument("-t", "--threshold", help="Threshold on the probabilities of prediction", type=float, default=0.1)
    args = parser.parse_args()
    paf_filepath = args.PAF
    output = args.Output
    threshold = args.threshold
    model = args.model
    overlap_list = Overlap_From_Paf(paf_filepath)
    graph = nx.Graph(overlap_list)
    nx.write_edgelist(graph, output + '-graph-edge-list')
    FeatureExtractor.Extract_All_Features(overlap_list, graph, output)
    classification_results = UseExistingClassifier.classifyoverlaps(output, model, threshold)
    FilterOverlaps.filter(paf_filepath, overlap_list, classification_results, output)
    print("Done")