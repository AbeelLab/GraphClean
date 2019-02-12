# Running GraphClean
## Getting Started

```sh
python GraphClean.py potato-overlaps.paf results/potato #Find and remove repeat induced overlaps in potato-overlaps.paf and print the normal overlaps to results/potato-newoverlaps.paf
python Graphclean.py potato-overlaps.paf results/potato -m models/model-potato-c0.01 -t 0.1 #Find and remove repeat induced overlaps in potato-overlaps.paf using models/model-potato-c0.01 model and 0.1 threshold and print the normal overlaps to results/potato-newoverlaps.paf
```

## Requirements
------------
* Python >= 3.5
* numpy >= 1.15.1
* networkx >= 2.2
* pandas >= 0.24.1

## Virtual environment
You can use the prepared conda environment for this project to run GraphClean
```
conda env create -f environment.yml
```
# GraphClean
Assembly graph cleaning through machine learning improves de novo long-read assembly. The following image shows the suggested steps for de novo assembly.

![alt text](images/pipeline.png)
