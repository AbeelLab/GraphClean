import numpy as np
from Bio import SeqIO
import sys
import os
import subprocess
from shutil import copyfile
from multiprocessing import Pool

print(sys.argv)
fasta_file = sys.argv[1]
output_directory = sys.argv[2]
aneusim_spec = sys.argv[3]
counter = int(sys.argv[4])
number_of_outputs = 1
number_of_ploidy = 4
coverage = 30
organism_name = os.path.basename(fasta_file)
seqnamelist = list()


def job(i):
    #SeqIO.write(subsample_sequence, fasta_file + "subsample.fasta-" + str(lensample) + '-' + str(i), "fasta")
    copyfile(fasta_file, fasta_file + "subsample.fasta-" + str(lensample) + '-' + str(i))
    input_fasta = fasta_file + "subsample.fasta-" + str(lensample) + '-' + str(i)
    aneusim_spec_new = aneusim_spec + '-' + organism_name + '-chr-' + str(seq.name) + '-' + str(lensample) + '-' + str(
        i)
    try:
        os.remove(aneusim_spec_new)
    except OSError:
        pass
    copyfile(aneusim_spec, aneusim_spec_new)
    with open(aneusim_spec_new, 'a') as aneusim_spec_file:
        for k in range(len(seqnamelist)):
            aneusim_spec_file.write('[' + seqnamelist[k] + ']\n')
            aneusim_spec_file.write('ploidy=' + str(number_of_ploidy) + "\n")
    base_dir_path = top_level_dir + "-" + str(lensample) + "-" + str(i)
    if not os.path.exists(base_dir_path):
        os.mkdir(base_dir_path)
    subprocess.call(
        "aneusim haplogen -s" + " " + aneusim_spec_new + " " + input_fasta + " " + base_dir_path, shell=True)
    subprocess.call("cat " + base_dir_path + "/*.fasta > " + base_dir_path + "/genome",
                                             shell=True)
    # base_dire genome pak kardam
    subprocess.call(
        'simlord --read-reference ' + fasta_file + "subsample.fasta-" + str(lensample) + '-' + str(
            i) + ' --coverage ' + str(coverage) + ' -pi 0.12 -pd 0.12 -ps 0.02 ' + base_dir_path + '/simlordreads',
        shell=True)
    print(base_dir_path + '/overlaps.paf')
    subprocess.call(
        'minimap2 -x ava-pb ' + base_dir_path + '/simlordreads.fastq ' + base_dir_path + '/simlordreads.fastq > ' + base_dir_path + '/overlaps.paf',
        shell=True)
    subprocess.call(
        'python LabelOverlaps.py ' + base_dir_path + '/overlaps.paf ' + base_dir_path + '/simlordreads.fastq.sam ' + str(
            coverage) + " " + organism_name + '-features-' + str(coverage) + "-" + str(lensample) + '-' + str(
            i), shell=True)


if __name__ == '__main__':
    lensample = 0
    for i, seq in enumerate(SeqIO.parse(open(fasta_file),'fasta')):
        seqnamelist.append(seq.name)
        lensample += len(seq)
    top_level_dir = output_directory + organism_name + '-ploidy' + str(number_of_ploidy) + '-cov-' + str(coverage)
    pool = Pool()
    #for i in range(number_of_outputs, number_of_outputs + 1):
    pool.map(job, range(counter, counter + number_of_outputs))
    pool.close()
    pool.join()
