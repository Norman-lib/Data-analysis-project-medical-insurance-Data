import pandas as pd

#This function is used to read data from a file
# Input: file name
# Output: data
def readData(fileName):
    df = pd.read_csv(r'./Train_Data.csv')
    return df