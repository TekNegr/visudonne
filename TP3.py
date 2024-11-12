############################DEFINITION##############################################################################################


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def get_data():
    data_test = pd.read_csv("c:/Users/hsoci/Desktop/devstar/visudonne/tp3/Testing_BOP.csv", sep=",")
    data_train = pd.read_csv("c:/Users/hsoci/Desktop/devstar/visudonne/tp3/Training_BOP.csv", sep=",")
    return data_test,data_train


############################CODE##############################################################################################

def show_data(data, type:str):
    print(f"{type} : \n \n ", data.head())

    choice = bool(int(input("Voulez vous la description ? \n 1 - OUI ; 0- NON \n")))

    if choice:
        print(data.describe())


    print(f"{type} has {data.shape[1]} COLS and {data.shape[0]} ROWS")


def show_missing_data(data, TYPE:str):
    print(f"For {TYPE}:\n")
    mean_miss_data = data.isnull().mean() *100
    print(mean_miss_data)
    print("\n\n")
    
def clean_data(data, TYPE:str):
    print("##################################################################\n BEFORE \n\n")
    show_missing_data(data, TYPE)
    
    for column in data.columns:
        if data[column].isnull().sum()>0:
            if data[column].dtype == "float64" or data[column].dtype == "int64":
                data[column].fillna(data[column].mean(), inplace=True)
            else:
                data[column].fillna("Unkown", inplace=True)
    data.drop(["deck_risk"], axis=1, inplace=True)
    data.drop(["oe_constraint"], axis=1, inplace=True)
    data.drop(["ppap_risk"], axis=1, inplace=True)
    data.drop(["stop_auto_buy"], axis=1, inplace=True)
    data.drop(["rev_stop"], axis=1, inplace=True)
    data.drop(["went_on_backorder"], axis=1, inplace=True)
    
    print("################################################################## \n AFTER \n\n")
    
    show_missing_data(data, TYPE)
    return data
    
    
def correlate_data(data, TYPE:str):
    print("Correlating data")
    data_encoded = pd.get_dummies(data, drop_first=True)
    data_sample = data_encoded.sample(frac=0.1)
    matrix_corr = data_sample.corr()
    print("done sampling")
    print(matrix_corr)
    # plt.figure()
    # sns.heatmap(matrix_corr, annot=True, fmt=".2f", cmap="coolwarm", square=True, cbar_kws={"shrink": .8})
    # plt.title("MATRICE DE CACA-RELATION")
    # plt.show()
    
    
    
def main():
    data_test, data_train = get_data()
    
    
    # show_data(data_train, "TRAINING")
    # show_data(data_test, "TESTING")
    
    # show_missing_data(data_train, "Training")
    # show_missing_data(data_test, "Testing")
    
    data_train = clean_data(data_train, "TRAINING")
    data_test = clean_data(data_test, "TESTING")
    
    correlate_data(data_train, "TRAINING")
    
if __name__ == "__main__":
    main()