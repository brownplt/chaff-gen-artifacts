
import numpy as np
import pandas as pd
from sklearn.cluster import AffinityPropagation



def text_clustering(texts, similarity):
    _similarity = similarity(texts)
    _affprop = AffinityPropagation(affinity="precomputed", damping=0.5, verbose=True,
        random_state=0, max_iter=500, convergence_iter=5)
    _affprop.fit(_similarity)
    return _affprop, _similarity


def print_clusters(affprop, texts):
    '''Print clusters'''
    texts = np.asarray(texts)
    clusters = np.unique(affprop.labels_)
    print(f'\n~ Number of texts:: {texts.shape[0]}')
    print(f'~ Number of clusters:: {clusters.shape[0]}')
    if clusters.shape[0] < 2: return 'Only few clusters - Stopped'


    clusters_as_dict = {}

    for cluster_id in clusters:
        exemplar = texts[affprop.cluster_centers_indices_[cluster_id]]
        cluster = np.unique(texts[np.nonzero(affprop.labels_==cluster_id)])
        cluster_str = '";\n  "'.join(cluster)
        print(f'\n# Cluster ({cluster_id}) with ({len(cluster)}) elements')
        print(f'Exemplar:: {exemplar}')
        print(f'\nOthers::\n  "{cluster_str}"')
        clusters_as_dict[cluster_id] = list(cluster)


    return clusters_as_dict

def get_cluster(text, clusters):
    
    for id in clusters:

        cs = [str(x) for x in clusters[id]]
        if text in cs: # clusters[id]:
            return id
    print('Text in NO cluster')
    print(text)
    return 0/0



def get_predictions(f, sheetname, clusters):

    df = pd.read_excel(f, sheet_name=sheetname)
    rows = df['Test Code'].to_numpy()
    return [get_cluster(code, clusters) for code in rows if not pd.isnull(code)]
