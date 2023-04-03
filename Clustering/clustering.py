import os
from sklearn.metrics.cluster import homogeneity_score, v_measure_score
import pandas as pd

from affinity_prop import text_clustering, print_clusters, get_predictions
from syntactic_similarity import tree_diff_metric, levenshtein

def read_excel_file(f, sheetname, check_fp = False):
    df = pd.read_excel(f, sheet_name=sheetname)
    df = df.reset_index()  # make sure indexes pair with number of rows

    fingerprints = []
    classifications = []
    code = []
    python_translation = []

    for _, row in df.iterrows():
        fp = row['Fingerprint']
        classification = row['Classification']
        c = row['Test Code']
        pt = row['Python Translation']

        fingerprinted = not pd.isnull(fp)
        not_all_fs = fingerprinted and len(set(list(fp))) > 1


        if fingerprinted and ( (not check_fp) or not_all_fs): 
            fingerprints.append(fp)
            classifications.append(classification)
            code.append(c)
            python_translation.append(pt)

    return fingerprints, classifications, code, python_translation


def print_metrics(labels_pred, labels_true):
    hs = homogeneity_score(labels_true, labels_pred)
    vm = v_measure_score(labels_true, labels_pred)

    msg = 'Sheet: {s} \t V Measure: {vm}, Homogeneity: {hs} '
    print(msg.format(hs = hs,vm = vm, s = s))


## TODO: CMD LINE ARGS!
if __name__ == "__main__":


    dir_path = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(dir_path, r"2020 Labelling and Clustering.xlsx")

    technique = 'tree_diff'

    sheets = [
        r'Docdiff-Consolidated-With-Code',
        r'Nile-Consolidated-With-Code',
        r'Filesystem-Consolidated-With-Co'
    ]

    for s in sheets:

        if technique == 'semantic':
            labels_pred, labels_true, _, __ = read_excel_file(file, s, check_fp=True)
        elif technique == 'levenshtein':

            # Affinity prop will strip fingerprints and clusters from labels. Need to corellate.

            _, labels_true, code, __ = read_excel_file(file, s)
            affprop, _ = text_clustering(code, similarity=levenshtein)
            cluster_dict = print_clusters(affprop, code)
            labels_pred = get_predictions(file, s, cluster_dict)
        
        elif technique == "tree_diff":
            _, labels_true, __, code = read_excel_file(file, s)
            affprop, _ = text_clustering(code, similarity=tree_diff_metric)
            cluster_dict = print_clusters(affprop, code)
            labels_pred = get_predictions(file, s, cluster_dict)
        else:
            print("UNKNOWN OPTION!")

        print_metrics(labels_pred=labels_pred, labels_true=labels_true)