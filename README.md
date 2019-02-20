# Running GraphClean
## Getting Started

```sh
#Downloading GraphClean
Git clone https://github.com/AbeelLab/GraphClean
cd GraphClean 
#Creating virtual env in the local directory with "conda_env" name
conda env create -f environment.yml -p=./conda_env
#activating virtual env
source activate conda_env/
#Find and remove repeat induced overlaps in potato-overlaps.paf and print the normal overlaps to results/potato-newoverlaps.paf
python GraphClean.py test/overlaps.paf results/potato 
#Find and remove repeat induced overlaps in potato-overlaps.paf using models/model-potato-c0.01 model and 0.1 threshold and print the normal overlaps to results/potato-newoverlaps.paf
python Graphclean.py test/overlaps.paf results/potato -m models/model-potato-c0.01 -t 0.1
```

## Requirements
------------
* Python >= 3.5
* numpy >= 1.15.1
* networkx >= 2.2
* pandas >= 0.24.1

## Usage
```sh
 usage: GraphClean detect remove induced overlaps in a paf file and remove them
        [-h] [-m MODEL] [-t THRESHOLD] PAF Output
 
 positional arguments:
   PAF                   Path to the input PAF file which contains overlaps
   Output                Output files prefix
 
 optional arguments:
   -h, --help            show this help message and exit
   -m MODEL, --model MODEL
                         Path to the model, models are inside models directory
   -t THRESHOLD, --threshold THRESHOLD
                         Threshold on the probabilities of prediction
``` 

## Virtual environment
You can use the prepared conda environment for this project to run GraphClean
```
conda env create -f environment.yml
```
# GraphClean
Assembly graph cleaning through machine learning improves de novo long-read assembly. The following image shows the suggested steps for de novo assembly.

![alt text](images/pipeline.png)
