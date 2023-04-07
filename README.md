# Artifacts: Conceptual Mutation Testing

This repository contains artifacts for the paper:

Conceptual Mutation Testing for Student Programming Misconceptions
by Siddhartha Prasad, Ben Greenman, Tim Nelson, and Shriram Krishnamurthi

and can be found at `https://github.com/brownplt/chaff-gen-artifacts`.


# Getting Started

Our artifacts mostly take the form of data. We include one executable component, which 
can be run as a Docker container. As a result, artifacts can be evaluated with only the 
following software:

- [Git ](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
  - Clone the repository by running: `git clone https://github.com/brownplt/chaff-gen-artifacts`

- Spreadsheet software able to open Open Document Spreadsheet (`.ods`) files (Microsoft Excel, LibreOffice, Google Sheets).
- A full installation of [Docker](https://docs.docker.com/get-docker/) and the Docker daemon.
  - Once you have installed Docker, fetch the relevant containers by running : 

```
docker pull sidprasad/wfe-clustering@sha256:334eacd2e1581d96285c0ce1c768f3c9670e59f906256792af41d8a7e70c8a7b
docker pull sidprasad/chaff-eval@sha256:29680a475ef9dccd3c2e665f617f64f74470a0435b33d653035bf9b3e1f2dcb6
docker pull sidprasad/fv-eval@sha256:2c68002e7c5a5dd749f466f0984eddf411a3956405da50807b697cb8a0ac4ef1
```

**Alternately**, you can build these containers from source (We recommend Docker version >= `20.10.14`)

```
cd Clustering
docker build . -t sidprasad/wfe-clustering:latest

cd ../ChaffEval
docker build . -t sidprasad/chaff-eval:latest

cd ../FeatureVectorExamination
docker build . -t sidprasad/fv-eval:latest
```


### Ensuring things work as expected:

Run a quick experiment, `docker run --rm -it sidprasad/wfe-clustering levenshtein DocDiff` to ensure Docker is installed
as expected.

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

- `AssignmentDecomposition/AssignmentCharacteristics.ods`: A decomposition of the 3 assignments under study (DocDiff, Nile, Filesystem) into characteristics deemed important by instructors and descriptions of mutant programs that violate these characteristics.
- `AssignmentDecomposition/DocDiff`: : Source code for these mutants (`Mutants` directory) alongside correct implementations of DocDiff (`Wheats` directory). There are 14 mutants and 2 wheats.
- `AssignmentDecomposition/Nile`: Source code for these mutants (`Mutants` directory) alongside correct implementations of Nile (`Wheats` directory). There are 12 mutants and 2 wheats.
- `AssignmentDecomposition/Filesystem` : Source code for these mutants (`Mutants` directory) alongside correct implementations of Filesystem (`Wheats` directory). There are 14 mutants and 2 wheats.

While this artifact consists of source code, the execution of this code is not required to evaluate this artifact. We present this artifact as data evidencing the decomposition of problems.


### Artifact 1.2: Labeled Submissions and Feature Vectors

This artifact can be found in the `Clustering` directory. It contains:

- `Clustering/Labelling and Clustering.ods`: While we do not share raw student submissions as part of our artifact, we provide a spreadsheet that provides relevant data. For each assignment, for each manually analyzed wheat failing example we provide:
    - An id for each wheat-failing-example ( identified by a session, timestamp, and line number.)
    - Relevant source code for the failing example in the Pyret language, alongside a Python translation (required for `GumTreeDiff`)
    - The misunderstanding label used as ground truth.
    - The corresponding feature vectors generated during semantic clustering.

We present this artifact as data documenting our manual labelling of WFEs.

### Artifact 1.3 : Cluster Evaluation

This artifact is presented as a Docker container that can be used to generate both semantic and syntactic clusters using this spreadsheet, and generate clustering evaluation metrics as described in the paper.. This container can either be run as follows:

```
docker run --rm -it sidprasad/wfe-clustering <option> <assignment>
```

where option can be one of `semantic`, `levenshtein` or `tree_diff`.
and assignment should match one of `DocDiff`, `Nile` or `Filesystem`

**Evaluating this artifact**: Depending on the provided option, this container should output V-Measure and Homogeneity scores represented in the paper.

- `levenshtein` : This option prints clusters alongside exemplars of each cluster. Finally, it prints V-Measure and Homogeneity of these clusters against ground truth. V-Measure and Homogeneity should not exceed*`Table 1` of the paper (when rounded).
- `tree_diff` : This option prints clusters alongside exemplars of each cluster. Finally, it prints V-Measure and Homogeneity of these clusters against ground truth. V-Measure and Homogeneity should not exceed* those in `Table 2` of the paper (when rounded).
- `semantic` : V-Measure and Homogeneity should match those in `Table 4` of the paper (when rounded).


*`levenshtein` and `tree_diff` clustering utlize Affinity Propagation (AP), which involves a degree of randomness. To mitigate the effect of randomness on the final clustering result, we ran AP multiple times, presenting the best-clustering result with respect to ground truth in Tables 1 and 2 of the paper. Even these best-results resulted in very low clustering correspondence.


### Artifact 1.4: Feature Vectors (Semantic CLusters) 
We provide the final results of feature vector generation for all student wheat failing examples by semantic clustering in the `FeatureVectorExamination` directory. We also provide a Docker container that can be used to evaluate these Feature Vectors.

This container can be run as follows:

```
docker run --rm -it sidprasad/fv-eval:latest <assignment>
```
where assignment should match one of `DocDiff`, `Nile` or `Filesystem`

**Evaluating this artifact**: Depending on the provided assignment, this container output  a list of the most common feature vectors per assignment in the paper, as well as WFE pass count.

- `docker run --rm -it sidprasad/fv-eval:latest DocDiff` : WFE pass counts should match those presented in `Table 8` of the paper. The top 6 largest clusters should match those in `Table 5` of the paper.

- `docker run --rm -it sidprasad/fv-eval:latest Nile` : WFE pass counts should match those presented in `Table 8` of the paper. The top 6 largest clusters should match those in `Table 6` of the paper.
- `docker run --rm -it sidprasad/fv-eval:latest Filesystem` : WFE pass counts should match those presented in `Table 8` of the paper. The top 6 largest clusters should match those in `Table 7` of the paper.

 
## Claim 2: Evidence that Chaffs selected using our clustering method out-performed expert-written mutants.

Our second contribution involved evaluating chaffs generated using our clustering process that out-performed expert-written chaffs that had been finetuned over several years. This was done by examining the feature vectors created by wheat failing examples against chaffs presented to students.

### Artifact 2.1

Chaffs presented to students for each assignment for each year are available in the `ChaffEval` directory. 
While this artifact consists of source code, the execution of this code is not required to evaluate this artifact. We present this artifact as data evidencing our choice of chaffs across years. The number of chaffs is as follows:

```
ChaffEval
│
├───DocDiff-Chaffs
│   ├───2020 (5 chaffs)
│   ├───2021 (5 chaffs)
│   └───2022 (5 chaffs)
├───Filesystem-Chaffs
│   ├───2020 (9 chaffs)
│   ├───2021 (9 Chaffs)
│   └───2022 (5 chaffs)
├───Nile-Chaffs
│   ├───2020 (9 chaffs)
│   ├───2021 (9 chaffs)
│   └───2022 (6 chaffs)
```


### Artifact 2.2

- Feature vectors generated by running each wheat failing example against its corresponding chaff set are presented in `ChaffEval\WFE-against-chaffs.ods`. We present this artifact as data evidencing our analysis of chaffs in 2022 against 2020 and 2021. These data are analyzed in Figure 4 and Table 9 of the paper.

This analysis can be re-run using a Docker container as follows:

```
docker run --rm -it sidprasad/chaff-eval:latest <assignment>
```

where assignment should match one of `DocDiff`, `Nile` or `Filesystem`.


**Evaluating this artifact**: Depending on the provided assignment, this container outputs a table comparing 1-m and 2-m wfes for handwritten chaffs (2020 and 2021) and generated chaffs (2022). It also displays the results of a 2-tailed Z test for statistical significance.


1-m and 2-m WFE pass counts should match those presented in `Figure 4` of the paper (when rounded). The results of a Z-test should match those presented in `Table 9` (when rounded).