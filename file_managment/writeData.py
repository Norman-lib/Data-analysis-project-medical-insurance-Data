#This function is used to write data to a file
# Input: file name, data to be written
# Output: None
def writeData(fileName, data):
    data.to_csv(fileName)