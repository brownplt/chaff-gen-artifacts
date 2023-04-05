# Artifacts: Conceptual Mutation Testing

TODO:
- [] Please use open formats for documents and preferably CSV or JSON for data.
- []  List of claims NOT supported by the artifact
- [] Found error in paper figure 3 (off by 1/ #N/A). If a WFE had no fingerprint, this was becasue (as Jack warned) it was impossible to identify the failing test in Pyret logs. In this case, we did not use these WFEs for our labelling or clustering analysis. 



This repository contains artifacts for the paper:


Conceptual Mutation Testing for Student Programming Misconceptions
by Siddhartha Prasad, Ben Greenman, Tim Nelson, and Shriram Krishnamurthi

and can be found at `https://github.com/brownplt/chaff-gen-artifacts`.


# Getting Started

Evaluating this artifact requires the following software:
- Microsoft Excel or an Equivalent spreadsheet software able to open `.xslx` files.
- [Docker ](https://docs.docker.com/get-docker/)


# Overview of Claims

Mutation testing for example suites is an effective way to make sure students solve the
right problem, but requires a carefully curated set of mutants. Prior work has left the
task of finding mutants entirely in the hands of experts, who often fail to anticipate
student misconceptions. Our work contributes:
- A method to generate effective mutants at low cost by clustering and analyzing incorrect examples
- Evidence that Chaffs selected using our clustering method out-performed expert-written mutants.

## Claim 1: A method to generate effective mutants at low cost by clustering and analyzing incorrect examples


The paper's first contribution involves a method that allows instructors to cluster and examine incorrect examples for student misunderstandings. In doing so, we looked at 3 assignments (DocDiff, Nile, and Filesystem) from an accelerated introduction to computer science course from 2020.
We then:
1. Collected wheat-failing-examples
2. Labelled a sample of these failing-examples with associated misunderstandings to generate 'ground truth'.
3. Employed and evaluated various techniques to cluster these examples, comparing them against ground truth. Various clustering techniques required:
     - *Syntactic Clustering*: Student example code
     - *Semantic Clustering*: 
         - Characteristics of a correct solution deemed important by instructors
         - Mutant programs that violate these characteristics.
         - Feature vector for each incorrect example, generated by running wheat-failing-examples against all mutant programs.


To this end, we provide the following artifacts. 

### Artifact 1.1: Decomposition of Problems

This artifact can be found in the `AssignmentDecomposition` directory. It contains:

- `AssignmentDecomposition\Characteristics to Chaff map.xlsx`: A decomposition of the 3 assignments under study (DocDiff, Nile, Filesystem) into characteristics deemed important by instructors, and descriptions of  mutant programs that violate these characteristics.
- `AssignmentDecomposition\DocDiff`, `AssignmentDecomposition\Nile`, `AssignmentDecomposition\Filesystem` : Source Code for these proposed mutants alongside correct implementations of the problem (wheats).


While this artifact consists of source code, the execution of this code is not required to evaluate this artifact. We present this artifact as data evidencing the decomposition of problems.


### Artifact 1.2: Labeled Submissions and Feature Vectors

This artifact can be found in the `Clustering` directory. It contains:

- `Clustering\2020 Labelling and Clustering.xlsx` (sheets: `DocDiff-Consolidated`, `Nile-Consolidated`, and `Filesystem-Consolidated`): While we do not share raw student submissions as part of our artifact, we provide a spreadsheet that provides relevant data. For each assignment, for each manually analyzed wheat failing example we provide:
    - An id for each wheat-failing-example ( identified by a session, timestamp, and line number.)
    - Relevant source code for the failing example in the Pyret language, alongside a Python translation (required for `GumTreeDiff`)
    - The misunderstanding label used as ground truth.
    - The corresponding feature vectors generated during semantic clustering.

We present this artifact as data documenting our manual labelling of WFEs. The number of labelled (classified) WFEs should match Figure 3 of the paper. 
 
### Artifact 1.3: Cluster Evaluation

This artifact is presented as a Docker container that can be used to generate both semantic and syntactic clusters using this spreadsheet, and generate clustering evaluation metrics as described in the paper.. This file can either be pulled from Dockerhub:

```
 docker pull sidprasad/wfe-clustering
```

or can be built from source in the `Clustering` directory, using the associated Dockerfile:

```
cd Clustering
docker build . -t sidprasad/wfe-clustering
```

It can then be run as follows:

```
docker run --rm -it sidprasad/wfe-clustering <option>
```

where option can be one of `semantic`, `leveshtein` or `tree_diff`.

**Evaluating this artifact**: Depending on the provided option, this container should output V-Measure and Homogeneity scores represented in the paper.

- `semantic` : V-Measure and Homogeneity should match Table 4 of the paper.
- `leveshtein` : V-Measure and Homogeneity should match Table 1 of the paper.
- `tree_diff` : V-Measure and Homogeneity should match Table 2 of the paper.

### Artifact 1.4: Semantic Clusters

This artifact is available in the  `Clustering\2020 Labelling and Clustering.xlsx` under the sheets `DocDiff-2020-Feature-Vectors`, `Nile-2020-Feature-Vectors`, and `Filesystem-2020-Feature-Vectors`. 
It contains the final results of clustering all student wheat failing examples by semantic clustering.
We do not, however, do not share student code, only unique identifiers for each WFE.
We present this artifact as data documenting our generation of feature vectors.

 
## Claim 2: Evidence that Chaffs selected using our clustering method out-performed expert-written mutants.


Our second contribution involved evaluating chaffs generated using our clustering process that out-performed expert-written chaffs that had been finetuned over several years. This was done by examining the feature vectors created by wheat failing examples against chaffs presented to students.

### Artifact 2.1

Chaffs presented to students for each assignment for each year are available in the `ChaffEval` directory. 
While this artifact consists of source code, the execution of this code is not required to evaluate this artifact. We present this artifact as data evidencing the decomposition of problems.


### Artifact 2.2

Feature vectors generated by running each wheat failing example against its corresponding chaff set are presented in `Chaff Eval\WFE-against-chaffs.xlsx`. 

We present this artifact as data evidencing our analysis of chaffs in 2022 against 2020 and 2021.
These data are analyzed in Figure 4 and Table 9 of the paper.
