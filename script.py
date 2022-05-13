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
    

def getinfo(ids, data):
    return [data[id] for id in ids]
    
def howmany(hasthis, incolumn, data):
    output = 0
    mydata = data[incolumn]
    for id in mydata.keys():
        if mydata[id] == hasthis:
            output += 1
    return output

def writetheage(data1, realdata):
    data = [realdata[i] for i in data1]
    exists = len(data) > 0
    if exists:
        print("    Av disse er:")
        agespresent = []
        for i in range(len(data)):
            if data[i]["age"] not in agespresent:
                agespresent.append(data[i]["age"])
        howmanyinages = {}
        numberanswered = len(data)
        for age in agespresent:
            howmanyinages[age] = 0
        for i in range(len(data)):
            howmanyinages[data[i]["age"]] += 1
        for age in howmanyinages.keys():
            print("    ", round((howmanyinages[age]/numberanswered)*100, 2), "%", "i aldersgruppen", age)

def writethelocation(data1, realdata):
    data = [realdata[i] for i in data1]
    exists = len(data) > 0
    if exists:
        print("    Av disse er:")
        locationspresent = []
        for i in range(len(data)):
            if data[i]["location"] not in locationspresent:
                locationspresent.append(data[i]["location"])
        howmanyinlocations = {}
        numberanswered = len(data)
        for location in locationspresent:
            howmanyinlocations[location] = 0
        for i in range(len(data)):
            howmanyinlocations[data[i]["location"]] += 1
        for location in howmanyinlocations.keys():
            print("    ", round((howmanyinlocations[location]/numberanswered)*100, 2), "%", "fra", location)

def writethegender(data1, realdata):
    data = [realdata[i] for i in data1]
    exists = len(data) > 0
    if exists:
        print("    Av disse er:")
        genderspresent = []
        for i in range(len(data)):
            if data[i]["gender"] not in genderspresent:
                genderspresent.append(data[i]["gender"])
        howmanyingenders = {}
        numberanswered = len(data)
        for gender in genderspresent:
            howmanyingenders[gender] = 0
        for i in range(len(data)):
            howmanyingenders[data[i]["gender"]] += 1
        for gender in howmanyingenders.keys():
            print("    ", round((howmanyingenders[gender]/numberanswered)*100, 2), "%", gender)

def writethebelief(data1, realdata):
    data = [realdata[i] for i in data1]
    exists = len(data) > 0
    if exists:
        print("    Av disse tror:")
        beliefspresent = []
        for i in range(len(data)):
            if data[i]["belief"] not in beliefspresent:
                beliefspresent.append(data[i]["belief"])
        howmanyinbeliefs = {}
        numberanswered = len(data)
        for belief in beliefspresent:
            howmanyinbeliefs[belief] = 0
        for i in range(len(data)):
            howmanyinbeliefs[data[i]["belief"]] += 1
        for belief in howmanyinbeliefs.keys():
            print("    ", round((howmanyinbeliefs[belief]/numberanswered)*100, 2), "%", belief)

def writeall(hasincreased, what, start, end, data, mystring):
    print(len(create_list(hasincreased, what, start, end, data)), mystring + ",", round((len(create_list(hasincreased, what, start, end, data)))/len(data.keys())*100, 2), "%", "av totalen")
    writetheage(create_list(hasincreased, what, start, end, data), data)
    writethelocation(create_list(hasincreased, what, start, end, data), data)
    writethegender(create_list(hasincreased, what, start, end, data), data)
    writethebelief(create_list(hasincreased, what, start, end, data), data)


data = get_data("data.csv")

converted = convert_data(data)

locations = []
for id in converted[1]["location"].keys():
    if converted[1]["location"][id] not in locations:
        locations.append(converted[1]["location"][id])

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

print("Av alle som har svart kommer:")
for location in locations:
    print(howmany(location, "location", converted[1]), "fra", location, ",\t", (howmany(location, "location", converted[1])/len(converted[0].keys()))*100, "%", "av totalen.")
print()
print("Vi har fått svar fra:")
for age in ["13-15 år", "16-17 år", "18-19 år"]:
    if howmany(age, "age", converted[1]) != 0:
        print(howmany(age, "age", converted[1]), "i aldersgruppen", age, ",\t", (howmany(age, "age", converted[1])/len(converted[0].keys()))*100, "%", "av totalen.")
print()
for gender in ["Mann", "Kvinne"]:
    if howmany(gender, "gender", converted[1]) != 0:
        print(howmany(gender, "gender", converted[1]), "har kjønnet", gender, ",\t", (howmany(gender, "gender", converted[1])/len(converted[0].keys()))*100, "%", "av totalen.")
print()
print("Om hvorvidt man mener skjermtid har økt fra før til etter pandemien svarer:")
for belief in ["Ja", "Nei"]:
    if howmany(belief, "belief", converted[1]) != 0:
        print(howmany(belief, "belief", converted[1]), belief, ",\t", (howmany(belief, "belief", converted[1])/len(converted[0].keys()))*100, "%", "av totalen.")
print()
print("Totalt har vi fått svar fra", len(converted[0].keys()), "personer")

print()
print()
writeall(True, "training", "before", "during", converted[0], "har trent mer under pandemien enn før den")
writeall(True, "training", "before", "after", converted[0], "har trent mer etter pandemien enn før den")
writeall(True, "training", "during", "after", converted[0], "har trent mer etter pandemien enn under den")
writeall(False, "training", "before", "during", converted[0], "har trent mindre under pandemien enn før den")
writeall(False, "training", "before", "after", converted[0], "har trent mindre etter pandemien enn før den")
writeall(False, "training", "during", "after", converted[0], "har trent mindre etter pandemien enn under den")
print()
writeall(True, "screen", "before", "during", converted[0], "har brukt skjerm mer under pandemien enn før den")
writeall(True, "screen", "before", "after", converted[0], "har brukt skjerm mer etter pandemien enn før den")
writeall(True, "screen", "during", "after", converted[0], "har brukt skjerm mer etter pandemien enn under den")
writeall(False, "screen", "before", "during", converted[0], "har brukt skjerm mindre under pandemien enn før den")
writeall(False, "screen", "before", "after", converted[0], "har brukt skjerm mindre etter pandemien enn før den")
writeall(False, "screen", "during", "after", converted[0], "har brukt skjerm mindre etter pandemien enn under den")