def changeValuesToBinary(data):
    data['smoker'].replace({'yes': True, 'no': False}, inplace=True)
    # print("yes")
    # for index, row in data.iterrows():
    #     print(row["smoker"]== "yes")
    #     if row["smoker"] == "yes":
    #         row["smoker"] = True
    #     elif row["smoker"] == "no":
    #         row["smoker"] = False
    return data