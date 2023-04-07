import os
import pandas as pd
import sys
import csv
import numpy as np


dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(dir_path, "data")

def read_csv(f):
    fingerprints = []
    with open(f, mode='r') as infile:
        reader = csv.reader(infile)


        # for rows in reader:
            
        #     #fv = rows[2]
        #     # We filter out rows with all 'm' during analysis.
        #     #all_m = len(set(list(fv))) == 1 and (fv[0] = 'm')

        #     if not all_m: 
        #         fingerprints.append(rows[2])


        fvs = [rows[1] for rows in reader if not ( len(set(list(rows[1]))) == 1 and (rows[1][0] == 'm') )  ]
    
    return fvs[1:]


def columnwise(fvs):

    xs = [ [ (1 if s == 'm' else 0) for s in fv ] for fv in fvs ]
    sums = [sum(row[i] for row in xs) for i in range(len(xs[0]))]

    return sums



def rank_clusters(xs):

    counts = { 
        x : xs.count(x)
        for x in xs
    }

    keys = list(counts.keys())
    values = list(counts.values())
    sorted_value_index = np.argsort(values)
    ranked = [(keys[i], values[i]) for i in sorted_value_index]
    ranked.reverse()
    return ranked

if __name__ == "__main__":


    if len(sys.argv) != 2:
         print("You supplied arguments : {l} \n Usage: <program> <assignment>. ".format(l= sys.argv))

    a = sys.argv[1]

    assignment = "{a}FV.csv".format(a = a)
    assignment = os.path.join(data_path, assignment)

    fvs = read_csv(assignment)
    
    
    print("WFE pass count for {a}. This should match Table 8.".format(a = a))
    wfepasscount = columnwise(fvs)
    print(wfepasscount, end=' ')

    ranked = rank_clusters(fvs)


    print("\n\nClusters for {a}".format(a = a))
    print("Count\tFeature Vector")

    for r in ranked:
        print("{c}\t{fv}".format(c = r[1], fv = r[0]))