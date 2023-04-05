
import numpy as np
import pandas as pd
import distance
import os
import json
import subprocess


dir_path = os.path.dirname(os.path.realpath(__file__))


in_container = os.environ.get('CONTAINER')

if not in_container:
    import docker
    client = docker.from_env()
    print("[No Gumtree installed, using GumTree docker container]")
else:
    print("[Running in Docker container]")


def exec_gumtree_tool(left, right):
    command = ["gumtree", "textdiff", "-f", "JSON", left, right]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    err = result.stderr.decode()

    if err is not None and len(err) > 0:
        return err
    
    output = result.stdout
    return output.decode()


def exec_gumtree_via_docker(left_base, right_base):

    assert(not in_container)
    vols = {
        left_base: {'bind': '/left', 'mode': 'rw'},
        right_base: {'bind': '/right', 'mode': 'rw'}
    }

    #  GumTree is hard to install. Instead, spin it up as a docker image.
    #  docker run -it -v scratch\left:/diff/left -v scratch\right:/diff/right -p 4567:4567 gumtreediff/gumtree textdiff -f JSON left/a.py right/a.py
    container = client.containers.run("gumtreediff/gumtree", "textdiff -f JSON /left/a.py /right/a.py", volumes = vols, detach=True)
    container.wait()
    output = container.logs()
    output = output.decode()
    container.remove() # Free container
    return output

def gumtree(t1, t2):

    def fix(txt):
        txt = ''.join(txt)
        txt = txt.replace('\\n', '\n')
        txt = txt.replace(r'_x000D_', '') #Carriage return in Excel
        #txt = txt.replace('\\r', '')
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
    
    # Exec and read results.

    # For each pair of texts, diff is the number of of 'actions' predicted by GumTree.

    if in_container:
        output = exec_gumtree_tool(left, right)

    else:
        output = exec_gumtree_via_docker(left_base, right_base)
    
    if ("'textdiff'" in output):
        print('Unexpected error in GumTree comparison!! There may be something wrong with the setup.')
        print(t1)
        print("-----------------")
        print(t2)
        print("-----------------")
        print(output)
        return 0/0

    as_dict = json.loads(output)
    return len(as_dict['actions'])

def tree_diff_metric(texts):
    # Affinity prop requires negative similarities, so returns -1 * tree_diff(t1, t2)
    texts = np.asarray(texts, dtype=object)

    _similarity = np.array([[gumtree(list(w1),list(w2)) for w1 in texts] for w2 in texts])
    _similarity = -1*_similarity
    _similarity = _similarity.astype(np.float64)
    return _similarity


def levenshtein(texts):
    # Affinity prop requires negative similarities, so returns -1 * levenshtein(t1, t2)

    texts = np.asarray(texts, dtype=object)
    _similarity = np.array([[distance.levenshtein(list(w1),list(w2)) for w1 in texts] for w2 in texts])
    _similarity = -1*_similarity
    _similarity = _similarity.astype(np.float64)
    return _similarity


