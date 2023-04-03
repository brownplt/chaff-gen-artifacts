import csv
import numpy as np
import pandas as pd
import distance
from sklearn.cluster import AffinityPropagation
from sklearn.metrics.cluster import rand_score, adjusted_rand_score, homogeneity_score, completeness_score, v_measure_score
import docker
import os
import json


client = docker.from_env()

dir_path = os.path.dirname(os.path.realpath(__file__))

def gumtree(t1, t2):

    def fix(txt):
        txt = ''.join(txt)
        txt = txt.replace('\\n', '\n')
        return txt

    def write_file(path, txt):
        
        with open(path, mode='w', encoding="utf8") as f:
            f.write(txt)

    t1 = fix(t1)
    t2 = fix(t2)

    base = os.path.join(dir_path, 'scratch')
    left_base = os.path.join(base, 'left')
    right_base = os.path.join(base, 'right')
    left = os.path.join(left_base, 'a.py')
    right = os.path.join(right_base, 'a.py')

    write_file(left, t1)
    write_file(right, t2)
    
    vols = {
        left_base: {'bind': '/left', 'mode': 'rw'},
        right_base: {'bind': '/right', 'mode': 'rw'}
    }

    # For each pair of texts, diff is the number of of 'actions' predicted by GumTree.

    #  GumTree is hard to install. Instead, spin it up as a docker image.
    #  docker run -it -v scratch\left:/diff/left -v scratch\right:/diff/right -p 4567:4567 gumtreediff/gumtree textdiff -f JSON left/a.py right/a.py
    container = client.containers.run("gumtreediff/gumtree", "textdiff -f JSON /left/a.py /right/a.py", volumes = vols, detach=True)

    container.wait()
    output = container.logs()
    output = output.decode()
    container.remove() # Free container
    
    if ("'textdiff'" in output):
        print('Unexpected error in GumTree comparison!! There may be something wrong with the setup.')
        print(t1)
        print("-----------------")
        print(t2)
        print("-----------------")
        return 0/0


    as_dict = json.loads(output)
    return len(as_dict['actions'])

def tree_diff_metric(texts):
    # Affinity prop requires negative similarities, so returns -1 * tree_diff(t1, t2)
    texts = np.asarray(texts, dtype=object)

    _similarity = np.array([[gumtree(list(w1),list(w2)) for w1 in texts] for w2 in texts])
    _similarity = -1*_similarity
    return _similarity


def levenshtein(texts):
    # Affinity prop requires negative similarities, so returns -1 * levenshtein(t1, t2)

    texts = np.asarray(texts, dtype=object)
    _similarity = np.array([[distance.levenshtein(list(w1),list(w2)) for w1 in texts] for w2 in texts])
    _similarity = -1*_similarity
    return _similarity

