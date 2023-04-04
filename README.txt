Mutation testing for example suites is an effective way to make sure students solve the
right problem, but requires a carefully curated set of mutants. Prior work has left the
task of finding mutants entirely in the hands of experts, who often fail to anticipate
student misconceptions [25].
Our work contributes:

1. A method to generate effective mutants at low cost by analyzing incorrect examples.
   - The up-front cost is to decompose a correct solution into characteristics. 
   - From there, the process is partially automated: use the characteristics to build a feature vector for each incorrect example, cluster the examples with
identical vectors, and derive mutants from the top-ranked vectors.

2. Using this process, we generated mutants in a few weeks (from thousands of
incorrect examples) that out-performed expert-written mutants that had been finetuned over several years. The method helps experts find semantically interesting errors
from student data which, in turn, can lead to better feedback and (eventually) better
learning outcomes for students.


# Contribution 1: A method to generate effective mutants at low cost by clustering and analyzing incorrect examples

## Cluster Evaluation

We then used these characteristics to build a feature vector for each wheat-failing example, cluster the examples with
identical vectors, and derive mutants from the top-ranked vectors. 


Excel spreadsheet that contains expert-labelled clusters, as well as the corresponding feature vectors for submissions in 2020.
Each wheat failing example is identified by a session, timestamp, and line number.

The following sheets contain tables linking each wheat failing example to a subproperty-based feature vector (also called a fingerprint)

- Docdiff-2020-Feature-Vectors
- Nile-2020-Feature-Vectors
- Filesystem-2020-Feature-Vectors

The following sheets contain a correspondence of each submission to its hand generated label, a conceptual fingerprint, alongside the relevant code used
for syntactic clustering.


- Docdiff-Consolidated-With-Code
- Nile-Consolidated-With-Code
- Filesystem-Consolidated-With-Code

These data were used to compute clustering metrics and compare  different clustering techniques.


## Decomposition of programs

The up-front cost is to decompose a correct solution into characteristics. We decomposed 3 assignments
(DocDiff, Nile, Filesystem) into characteristics, and determined chaff-programs to characterize each characteristic.

These can be found here: https://drive.google.com/drive/u/1/folders/1H8A5u0YUxECt_1spWbq6zod3nC3qL2UM







## 2020, 2021, 2022 Comparison of results

https://drive.google.com/drive/u/1/folders/1OCQs6m2C9TMhRgr41MmwGTX8MS0jFkMx

This is where we get wheats and chaffs

