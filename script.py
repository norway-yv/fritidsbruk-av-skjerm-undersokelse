"""Documentation"""
# (c) Yrjar Vederhus, 2022
# get_data:
    # Returns pandas dataframe with the raw csv data from variable filename. filename must be str, the name or path of the csv file you want a dataframe from
#convert_data:
    #Returns tuple.
    #tuple[0] is dictionary given as 
    # {
    #   id: {
    #       "age": age, 
    #       "gender": gender, 
    #       "location": location, 
    #       "training": {
    #           "before": before,
    #           "during": during,
    #           "after": after
    #        },
    #        "screen": {
    #            "before": before,
    #            "during": during,
    #            "after": after
    #        }
    #   }, 
    #   id: {
    #       and so on
    #   }
    # }
    #Where id is the id of the user, age is the age of the user, and so on. It is given in norwegian as the alternatives in the Forms form.


import pandas as pd

def get_data(filename):
    """Returns pandas element with csv data from filename. filename is str, .csv file"""
    data = pd.read_csv(filename)
    return data

def convert_data(data):
    """Returns dataframe data as dictionaries in tuple, element 0 is indexed by ID, element 1 by header"""
    #Get row of data
    data_list = data.values.tolist()
    by_id = {}
    for row in data_list:
        by_id[row[0]] = {}
        by_id[row[0]]["age"] = row[6]
        by_id[row[0]]["gender"] = row[7]
        by_id[row[0]]["location"] = row[8]
        by_id[row[0]]["training"] = {
            "before": row[9],
            "during": row[10],
            "after": row[11]
        }
        by_id[row[0]]["screen"] = {
            "before": row[12],
            "during": row[13],
            "after": row[14]
        }
        by_id[row[0]]["belief"] = row[15]
        

    by_column = {}
    column_names = ["age", "gender", "location"]
    for name in column_names:
        by_column[name] = {}
        for id in by_id.keys():
            by_column[name][id] = by_id[id][name]
    by_column["training"] = {}
    by_column["screen"] = {}
    for id in by_id.keys():
        by_column["training"][id] = by_id[id]["training"]
        by_column["screen"][id] = by_id[id]["screen"]
    by_column["belief"] = {}
    for id in by_id.keys():
        by_column["belief"][id] = by_id[id]["belief"]
    
    return (by_id, by_column)
    

data = get_data("data.csv")

converted = convert_data(data)
print(converted[0])
print(converted[1])