
import numpy as np
import pandas as pd
import distance
import os
import json
import subprocess
from tqdm import tqdm
import sys
import uuid


dir_path = os.path.dirname(os.path.realpath(__file__))


in_container = os.environ.get('CONTAINER')

if not in_container:
    import docker
    client = docker.from_env()
    print("[No Gumtree installed, using GumTree docker container]")
else:
    print("[Running in Docker container]")



def get_filename():
    u = uuid.uuid4().hex
    fn = "{u}.py".format(u = u)
    return os.path.join(dir_path, fn)

def write_file(path, txt):
    with open(path, mode='w', encoding="utf8") as f:
        f.write(txt)

def fix(txt):
    txt = ''.join(txt)
    txt = txt.replace('\\n', '\n')
    txt = txt.replace(r'_x000D_', '') #Carriage return in Excel
    return txt

def exec_gumtree_tool(left, right):
    command = ["gumtree", "textdiff", "-f", "JSON", left, right]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    err = result.stderr.decode()

    if err is not None and len(err) > 0:
        return err
    
    output = result.stdout
    x =  output.decode()
    return x


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

def gumtree(left, right):

    
    # Exec and read results.

    # For each pair of texts, diff is the number of of 'actions' predicted by GumTree.

    if in_container:
        output = exec_gumtree_tool(left, right)

    else:
         #output = exec_gumtree_via_docker(left_base, right_base)
         print("No longer supported. Can run in container only.")
    
    if ("'textdiff'" in output):
        print('Unexpected error in GumTree comparison!! There may be something wrong with the setup.')
        print(output)
        sys.exit(-1)

    as_dict = json.loads(output)
    return len(as_dict['actions'])

def tree_diff_metric_(texts):
    # Affinity prop requires negative similarities, so returns -1 * tree_diff(t1, t2)
    texts = np.asarray(texts, dtype=object)

    _similarity = np.array([[gumtree(list(w1),list(w2)) for w1 in texts] for w2 in texts])
    _similarity = -1*_similarity
    _similarity = _similarity.astype(np.float64)
    return _similarity


def levenshtein_(texts):
    # Affinity prop requires negative similarities, so returns -1 * levenshtein(t1, t2)

    texts = np.asarray(texts, dtype=object)
    _similarity = np.array([[distance.levenshtein(list(w1),list(w2)) for w1 in texts] for w2 in texts])
    _similarity = -1*_similarity
    _similarity = _similarity.astype(np.float64)
    return _similarity



def tree_diff_metric(texts):
    texts = np.asarray(texts, dtype=object)
    _similarity = []



    def setup_file(t):
        t = fix(t)
        fn = get_filename()
        write_file(fn, t)
        return fn
    
    filenames = np.array([ setup_file(x) for x in texts])

    for w2 in tqdm(filenames):
        xx = lambda w1 : gumtree(w1,w2) 
        arr = list(map(xx, filenames))

        _similarity.append(np.array(arr))


    _similarity = np.stack( _similarity, axis=0 )
    _similarity = -1*np.array(_similarity)
    _similarity = _similarity.astype(np.float64)
    return _similarity



# TODO: This is the future, need to figure it out.
def levenshtein(texts):
    # Affinity prop requires negative similarities, so returns -1 * levenshtein(t1, t2)

    texts = np.asarray(texts, dtype=object)
    _similarity = []



    for w2 in tqdm(texts):

        xx = lambda w1 : distance.levenshtein(list(w1),list(w2)) 


        #dist = np.vectorize( )
        #arr = lit(map(dist,texts))
        arr = list(map(xx, texts))

        _similarity.append(np.array(arr))


    _similarity = np.stack( _similarity, axis=0 )
    _similarity = -1*np.array(_similarity)
    _similarity = _similarity.astype(np.float64)
    return _similarity



