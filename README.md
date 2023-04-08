# Artifacts: Conceptual Mutation Testing

This repository contains artifacts for the paper:

Conceptual Mutation Testing for Student Programming Misconceptions
by Siddhartha Prasad, Ben Greenman, Tim Nelson, and Shriram Krishnamurthi

and can be found at `https://github.com/brownplt/chaff-gen-artifacts`.


- [Artifacts: Conceptual Mutation Testing](#artifacts-conceptual-mutation-testing)
- [Getting Started](#getting-started)
    - [Ensuring things work as expected:](#ensuring-things-work-as-expected)
- [\[Optional\] Running all executable components](#optional-running-all-executable-components)
- [Overview of Claims](#overview-of-claims)
  - [Claim 1: A method to generate effective mutants at low cost by clustering and analyzing incorrect examples](#claim-1-a-method-to-generate-effective-mutants-at-low-cost-by-clustering-and-analyzing-incorrect-examples)
    - [Artifact 1.1: Decomposition of Problems](#artifact-11-decomposition-of-problems)
    - [Artifact 1.2: Labeled Submissions and Feature Vectors](#artifact-12-labeled-submissions-and-feature-vectors)
    - [Artifact 1.3 : Cluster Evaluation](#artifact-13--cluster-evaluation)
    - [Artifact 1.4: Feature Vectors (Semantic Clusters)](#artifact-14-feature-vectors-semantic-clusters)
  - [Claim 2: Evidence that Chaffs selected using our clustering method out-performed expert-written mutants.](#claim-2-evidence-that-chaffs-selected-using-our-clustering-method-out-performed-expert-written-mutants)
    - [Artifact 2.1](#artifact-21)
    - [Artifact 2.2](#artifact-22)


# Getting Started

Our artifacts mostly take the form of data. We include 3 executable components, which 
can be run as a Docker container. As a result, artifacts can be evaluated with only the 
following software:

- [Git ](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
  - Clone the repository by running: `git clone https://github.com/brownplt/chaff-gen-artifacts`

- Spreadsheet software able to open Open Document Spreadsheet (`.ods`) files (Microsoft Excel, LibreOffice, Google Sheets).
- A full installation of [Docker](https://docs.docker.com/get-docker/) and the Docker daemon.
  - Once you have installed Docker, fetch the relevant containers by running : 


```
docker pull sidprasad/wfe-clustering:latest
docker pull sidprasad/chaff-eval:latest
docker pull sidprasad/fv-eval:latest
```

Ensure that images have the following sha256 digests, by running `docker images --digests`. You should see the following in the table:


```
REPOSITORY                 TAG       DIGEST                                                                    
sidprasad/fv-eval          latest    sha256:daf0985f374f6675b72de2191a4c67d84b1eb0a823bff8edc15c5bf83027b1f6   
sidprasad/chaff-eval       latest    sha256:29680a475ef9dccd3c2e665f617f64f74470a0435b33d653035bf9b3e1f2dcb6  
sidprasad/wfe-clustering   latest    sha256:08ce554b9d63a48b2e16fc0f953dce3801a5d1ad5978cadb31b195833d499b69
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

Note that if you build these from source, digests will differ from prebuilt images.

Additionally, we include a script that requires the use of a Unix-like command line shell. However, this is not required to evaluate the artifact.

### Ensuring things work as expected:

Run a quick experiment, execute the following to ensure Docker is installed as expected. 

- `docker run --rm -it sidprasad/wfe-clustering levenshtein DocDiff` This should print text in clusters, a V Measure score, and a Homogeneity score.
- `docker run --rm -it sidprasad/chaff-eval DocDiff`: This may take a few minutes to run, and should output 2 tables.
- `docker run --rm -it sidprasad/fv-eval DocDiff`: This should output A list as well as a large table.


# [Optional] Running all executable components

The sections below describe data and executable components that comprise this artifact,
alongside how to evaluate these components. We recommend following these guidelines in order.
However, if you would rather *first* run *all* executable components, you can do so by running
the `run-all.sh` script.

Since it launches several long-running containers, this script will take several hours to run. In our experience it may take as long as 16 hours. This script captures executable output in the following files: 


- wfe-clustering-semantic-DocDiff.txt
- wfe-clustering-semantic-Nile.txt
- wfe-clustering-semantic-Filesystem.txt
- wfe-clustering-levenshtein-DocDiff.txt
- wfe-clustering-levenshtein-Nile.txt
- wfe-clustering-levenshtein-Filesystem.txt
- wfe-clustering-tree_diff-DocDiff.txt
- wfe-clustering-tree_diff-Nile.txt
- wfe-clustering-tree_diff-Filesystem.txt

These can be evaluated as described in the section [Artifact 1.3 : Cluster Evaluation](#artifact-13--cluster-evaluation).

- fv-eval-DocDiff.txt
- fv-eval-Nile.txt
- fv-eval-Filesystem.txt

These can be evaluated as described in the section [Artifact 1.4: Feature Vectors (Semantic Clusters)](#artifact-14-feature-vectors-semantic-clusters)

- chaff-eval-DocDiff.txt
- chaff-eval-Nile.txt
- chaff-eval-Filesystem.txt
These can be evaluated as described in the section [Artifact 2.2](#artifact-22)


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
and assignment should match one of `DocDiff`, `Nile` or `Filesystem`.

`levenshtein` and `tree_diff` clustering are quite resource intensive, and may take several minutes to a few hours to complete. As a result, we display progress bars as a convenience when using these options. These  look something like:

```
Clustering by levenshtein
Clustering data from Nile
  1%█▋             | 1/122 [00:26<53:34, 26.56s/it]
```

**Evaluating this artifact**: Depending on the provided option, this container should output V-Measure and Homogeneity scores represented in the paper.

- `levenshtein` : This option prints clusters alongside exemplars of each cluster. Finally, it prints V-Measure and Homogeneity of these clusters against ground truth. V-Measure and Homogeneity should not exceed*`Table 1` of the paper (when rounded).
- `tree_diff` : This option prints clusters alongside exemplars of each cluster. Finally, it prints V-Measure and Homogeneity of these clusters against ground truth. V-Measure and Homogeneity should not exceed* those in `Table 2` of the paper (when rounded).
- `semantic` : V-Measure and Homogeneity should match those in `Table 4` of the paper (when rounded).


*`levenshtein` and `tree_diff` clustering utlize Affinity Propagation (AP), which involves a degree of randomness. To mitigate the effect of randomness on the final clustering result, we ran AP multiple times, presenting the best-clustering result with respect to ground truth in Tables 1 and 2 of the paper. Even these best-results resulted in very low clustering correspondence.


### Artifact 1.4: Feature Vectors (Semantic Clusters) 
We provide the final results of feature vector generation for all student wheat failing examples by semantic clustering in the `FeatureVectorExamination` directory. We also provide a Docker container that can be used to evaluate these Feature Vectors.

This container can be run as follows:

```
docker run --rm -it sidprasad/fv-eval:latest <assignment>
```
where assignment should match one of `DocDiff`, `Nile` or `Filesystem`. Example output should look like:

```
WFE pass count for DocDiff. This should match Table 8.
[148, 117, 0, 126, 57, 92, 71, 85, 131, 186, 280, 195, 120, 111]

Clusters for DocDiff
Count   Feature Vector
800     dddddddddddddd
68      dddddddddmdddd
66      mddddddddmdddd
52      ddddmddddddddd
49      dddmdddddddddd
48      mddddddddddddd
48      ddddddddddmdmm
38      dddddddddmdmdd
30      dddddddddddddm
28      dmdddddmmdmmdd
24      dddddmdddddddd
23      ddddddmddddddd
22      dmdddddddddddd
20      dmdddmdmmdmddd
15      ddddddddddmddd
15      dmdddmdmmdmmdd
13      mddddddddmdmdd
13      ddddddddddddmd
13      ddddddmdddmmmm
12      ddddddddddmmmm
11      dddmddddmdmmdd
11      dddmddmdmdmmdd
9       dddmddmdmdmddd
9       mddddddmmdmddd
6       dmdmdddddddddd
6       dddmdmddddmmmd
6       dddmddddddmmmd
6       dddmddddddmmdd
5       dddmdmddmdmmmd
5       mdddmddddddddd
5       ddddddmdddmddd
5       dddmddmdddmmdd
4       dmdddddmmdmddd
4       dddmdmddddmdmd
4       dmddddddddmmdd
4       ddddddddmdmddd
3       dmdddmddmdmddd
3       ddddddddddmdmd
3       dmdddmddmdmmdd
3       mdddddddmdmddd
3       dmdddddmddmmmm
3       dddmddmddddddd
3       dddddmddddmmdd
2       dmdddmddddmmdd
2       dmdddddmddmmmd
2       ddddddmdddmdmm
2       ddddddddddmmdd
2       dddddmddmdmddd
1       dmdmdddddddddm
1       mdddddddddmddd
1       mddddddmddmddd
1       dddmdmddmdmmdd
1       dmdddddmddmmdd
1       dddddmddmdmmdd
1       dddmdmdddddddm
1       mmdddddddddddd
1       dmdmdddmddmmmd
1       ddddddddmdmmdd
1       dddmddddddmddd
1       dmdddmddddmddd
1       dddddmddddmmmm
1       ddddddddddmmmd
1       mddddddmmmmddd
```

**Evaluating this artifact**: Depending on the provided assignment, this container output  a list of the most common feature vectors per assignment in the paper, as well as WFE pass count.

- `docker run --rm -it sidprasad/fv-eval:latest DocDiff` : WFE pass counts should match those presented in `Table 8` of the paper. The top 6 largest clusters should match those in `Table 5` of the paper. If two clusters had the same size, we chose an illustrative example in `Table 5`.  

- `docker run --rm -it sidprasad/fv-eval:latest Nile` : WFE pass counts should match those presented in `Table 8` of the paper. The top 6 largest clusters should match those in `Table 6` of the paper.
- `docker run --rm -it sidprasad/fv-eval:latest Filesystem` : WFE pass counts should match those presented in `Table 8` of the paper. However, we discovered an error in our script while packaging artifacts for evaluation. As a result, the top 6 clusters for Filesystem should look as follows:

```
Count   Feature Vector
2502    dddddddddddddd
232     dddmdddddddddd
190     ddddddddmddddd
63      mmdmmmmmmmmddm
53      ddmdddddddddmd
35      ddddddmddddddd
```

`Table 7` of the paper will be updated to match this in the final paper revision.

 
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

Example output should look like:

```
Assignment      Number of WFEs          WFEs in 1-m or 2-m clusters
Filesystem-2020 3359                    144 (4.286990175647514%)
Filesystem-2021 3121                    145 (4.645946811919257%)
Filesystem-2022 895                     105 (11.731843575418994%)


Evaluation for Statistical Significance using a 2-tailed Z test:
Filesystem-2021 vs Filesystem-2020:     p = 0.25205576349493997  Z = -0.6680345680639307         d = -0.016267758450340192       with CI : [-0.06  0.03]
Filesystem-2022 vs Filesystem-2020:     p = 2.354439491365171e-10        Z = -6.228511377531537  d = -0.28138932858170806        with CI : [-0.35 -0.21]
Filesystem-2022 vs Filesystem-2021:     p = 2.318715159624573e-09        Z = -5.859686061058633  d = -0.25951207993446357        with CI : [-0.33 -0.19]
```


**Evaluating this artifact**: Depending on the provided assignment, this container outputs a table comparing 1-m and 2-m wfes for handwritten chaffs (2020 and 2021) and generated chaffs (2022). It also displays the results of a 2-tailed Z test for statistical significance.


- `docker run --rm -it sidprasad/chaff-eval:latest DocDiff`: 1-m and 2-m WFE pass counts should match those presented in `Figure 4` of the paper (when rounded). The results of a Z-test should match those presented in `Table 9` (when rounded).


- `docker run --rm -it sidprasad/chaff-eval:latest Nile`: 1-m and 2-m WFE pass counts should match those presented in `Figure 4` of the paper (when rounded). The results of a Z-test should match those presented in `Table 9` (when rounded).

  
- `docker run --rm -it sidprasad/chaff-eval:latest Filesystem`:  Output should be as follows:

```
Assignment      Number of WFEs          WFEs in 1-m or 2-m clusters
Filesystem-2020 3359                    144 (4.286990175647514%)
Filesystem-2021 3121                    145 (4.645946811919257%)
Filesystem-2022 895                     105 (11.731843575418994%)


Evaluation for Statistical Significance using a 2-tailed Z test:
Filesystem-2021 vs Filesystem-2020:     p = 0.25205576349493997  Z = -0.6680345680639307         d = -0.016267758450340192       with CI : [-0.06  0.03]
Filesystem-2022 vs Filesystem-2020:     p = 2.354439491365171e-10        Z = -6.228511377531537  d = -0.28138932858170806        with CI : [-0.35 -0.21]
Filesystem-2022 vs Filesystem-2021:     p = 2.318715159624573e-09        Z = -5.859686061058633  d = -0.25951207993446357        with CI : [-0.33 -0.19]
```

This is because we discovered an error in our script counting WFEs for Filesystem 2020 while packaging artifacts for evaluation.  `Figure 4` and `Table 9` will be updated accordingly in the final paper revision.