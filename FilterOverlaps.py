import re

def Overlap_From_Paf(line):
    line = line[:-1].split()
    read1 = int(re.search(r'\d+', line[0]).group())
    read2 = int(re.search(r'\d+', line[5]).group())
    return [read1, read2]

def filter(overlap_file ,overlap_list, labels, outputpath):
    outputpath = outputpath + '-newoverlaps.paf'
    read_label_dict = dict(zip(overlap_list, labels))
    with open(outputpath, 'w') as output:
        with open(overlap_file) as ov_file:
                for line in ov_file:
                    reads = Overlap_From_Paf(line)
                    name = (reads[0], reads[1])
                    if name in read_label_dict.keys():
                        if read_label_dict[name] == 0:
                            output.write(line)
                    else:
                        name = (reads[1], reads[0])
                        if name in read_label_dict.keys():
                            if read_label_dict[name] == 0:
                                output.write(line)
                        else:
                            output.write(line)