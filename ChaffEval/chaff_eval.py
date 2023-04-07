import os
from sklearn.metrics.cluster import homogeneity_score, v_measure_score
import pandas as pd

import sys

import scipy.stats
import math
import pingouin as pg

# calculate the Cohen's d between two samples
from numpy.random import randn
from numpy.random import seed
from numpy import mean
from numpy import var
from math import sqrt


dir_path = os.path.dirname(os.path.realpath(__file__))
ods = os.path.join(dir_path, r"WFE-against-chaffs.ods")

def read_excel_file(f, sheetname):
    df = pd.read_excel(f, sheet_name=sheetname, engine="odf")
    #df = df.reset_index()  # make sure indexes pair with number of rows

    arr = df.to_numpy()


    x = list(arr[0])
    #return fingerprints, classifications, code, python_translation
    return [ list(row[1:]) for row in arr]


def z_score(d_control, d_variation):

    n_control = len(d_control)
    n_variation = len(d_variation)

    control_p = sum(d_control) / n_control
    variation_p = sum(d_variation) / n_variation

    # Std err
    control_se = math.sqrt((control_p*(1-control_p)/n_control))
    variation_se = math.sqrt((variation_p*(1-variation_p)/n_variation))

    z = (control_p-variation_p)/math.sqrt(math.pow(control_se,2)+math.pow(variation_se,2))
    return z

def cohend(control, variation):
    nc, nv = len(control), len(variation)
    stat = pg.compute_effsize(control, variation, False, eftype='cohen')
    ci = pg.compute_esci(stat=stat, nx=nc, ny=nv, eftype='cohen')

    return stat, ci

def get_1_2_ms(fvs):
    return [v for v in fvs if v.count("m") == 1 or v.count("m") == 2]

def gen_fig_4(fvs_sets):
    
    print("Assignment\tNumber of WFEs\t\tWFEs in 1-m or 2-m clusters")
    for (a, fv_set) in fvs_sets:
        num_wfes = len(fv_set)
        imp_wfe = len(get_1_2_ms(fv_set))
        percent = imp_wfe/num_wfes * 100

        print("{a}\t{nw}\t\t\t{iw} ({p}%)".format(a = a, nw = num_wfes, iw = imp_wfe, p = percent))



def gen_fig_9(fvs_sets):



    data = { a : [0]* len(fv_set) + [1]*len(get_1_2_ms(fv_set)) for  (a, fv_set) in fvs_sets}

    for y1 in data:
        for y2 in data:
            if y1 < y2:
                control = data[y1]
                variation = data[y2]

                z = z_score(control, variation)
                p = scipy.stats.norm.sf(abs(z))

                d, ci = cohend(control, variation)


                print('{y2} vs {y1}:\tp = {p}\t Z = {z}\t d = {d}\t with CI : {ci}'.format(y2 = y2, y1 = y1, z = z, d = d, p = p, ci = ci))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("You supplied arguments : {l} \n Usage: <program> <assignment>. ".format(l= sys.argv))

    assignment = sys.argv[1]


    sheets = [ assignment+'-2020', assignment+'-2021', assignment+'-2022' ]
    fvs_sets = [ (s, read_excel_file(ods, s)) for s in sheets ]

    print("Comparing 1-m and 2-m wfes for handwritten chaffs (2020 and 2021) and generated chaffs (2022).\n")
    gen_fig_4(fvs_sets)


    print("\n\nEvaluation for Statistical Significance using a 2-tailed Z test:")
    gen_fig_9(fvs_sets)



