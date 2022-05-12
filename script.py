#Programmet er på engelsk for å kunne hjelpes av Tabnine, Kite, og GitHub Copilot. Dokumentasjonen er på engelsk for GitHub Copilot som leser hele programmet.

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
import matplotlib.pyplot as plt

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

def number_options(column, data):
    """I'm not going to document anything. As long as I understand it next week I am happy."""
    if column == "training":
        output = {"Mindre enn 2 timer per uke": {"before": 0, "during": 0, "after": 0}, "2-4 timer per uke": {"before": 0, "during": 0, "after": 0}, "4-6 timer per uke": {"before": 0, "during": 0, "after": 0}, "Mer enn 6 timer per uke": {"before": 0, "during": 0, "after": 0}}
    elif column == "screen":
        output = {"Mindre enn 1 time": {"before": 0, "during": 0, "after": 0}, "1-3 timer": {"before": 0, "during": 0, "after": 0}, "3-5 timer": {"before": 0, "during": 0, "after": 0}, "5-8 timer": {"before": 0, "during": 0, "after": 0}, "Mer enn 8 timer": {"before": 0, "during": 0, "after": 0}}
    mydata = data[column]
    for id in mydata.keys():
        for time in ["before", "during", "after"]:
            output[mydata[id][time]][time] += 1

    return output

def create_list(hasincreased, what, start, end, data):
    output = []
    if what == "training":
        reference = ["Mindre enn 2 timer per uke", "2-4 timer per uke", "4-6 timer per uke", "Mer enn 6 timer per uke"]
    elif what == "screen":
        reference = ["Mindre enn 1 time", "1-3 timer", "3-5 timer", "5-8 timer", "Mer enn 8 timer"]
    
    for id in data.keys():
        isgreater = reference.index(data[id][what][start]) < reference.index(data[id][what][end])
        if (hasincreased and isgreater):
            output.append(id)
        issmaller = reference.index(data[id][what][start]) > reference.index(data[id][what][end])
        if (not hasincreased and issmaller):
            output.append(id)
    return output
    




data = get_data("data.csv")

converted = convert_data(data)
"""
print(converted[0])
print(converted[1])
print()
print(number_options("training", converted[1]))
"""
number_options_output = number_options("training", converted[1])
for key in number_options_output.keys():
    if number_options_output[key] != {"before": 0, "during": 0, "after": 0}:
        plt.plot(["Før pandemien", "Under pandemien", "Etter pandemien"], number_options_output[key].values(), label=key)
plt.legend()
plt.title("Hvor mange som trener hvor mye før, under, og etter pandemien")
plt.ylabel("Antall personer")
plt.show()


number_options_output = number_options("screen", converted[1])
for key in number_options_output.keys():
    if number_options_output[key] != {"before": 0, "during": 0, "after": 0}:
        plt.plot(["Før pandemien", "Under pandemien", "Etter pandemien"], number_options_output[key].values(), label=key)
plt.legend()
plt.title("Hvor mange som bruker skjerm på fritiden hvor mye før, under, og etter pandemien")
plt.ylabel("Antall personer")
plt.show()

print("Her kommer litt statistikk:")
print(len(create_list(True, "training", "before", "during", converted[0])), "har trent mer under pandemien enn før den")
print(len(create_list(True, "training", "before", "after", converted[0])), "har trent mer etter pandemien enn før den")
print(len(create_list(True, "training", "during", "after", converted[0])), "har trent mer etter pandemien enn under den")
print(len(create_list(False, "training", "before", "during", converted[0])), "har trent mindre under pandemien enn før den")
print(len(create_list(False, "training", "before", "after", converted[0])), "har trent mindre etter pandemien enn før den")
print(len(create_list(False, "training", "during", "after", converted[0])), "har trent mindre etter pandemien enn under den")
print()
print(len(create_list(True, "screen", "before", "during", converted[0])), "har brukt skjerm mer under pandemien enn før den")
print(len(create_list(True, "screen", "before", "after", converted[0])), "har brukt skjerm mer etter pandemien enn før den")
print(len(create_list(True, "screen", "during", "after", converted[0])), "har brukt skjerm mer etter pandemien enn under den")
print(len(create_list(False, "screen", "before", "during", converted[0])), "har brukt skjerm mindre under pandemien enn før den")
print(len(create_list(False, "screen", "before", "after", converted[0])), "har brukt skjerm mindre etter pandemien enn før den")
print(len(create_list(False, "screen", "during", "after", converted[0])), "har brukt skjerm mindre etter pandemien enn under den")
print()