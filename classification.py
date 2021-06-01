from pycaret.classification import *


def build_classifier(df,label):
    m1 = setup(data = df,target = label,silent =True)
    best = compare_models()
    table = pull()
    return table