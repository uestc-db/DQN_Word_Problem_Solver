import json

reject = []
temp = {}
with open("ai2rel", "r") as f:
   lines = f.readlines()
   for line in lines:
       line = line[:line.find('\n')]
       if not line:
           continue      
       if "index" in line:
           temp["index"] = int(line[7:])
       elif "Interest" in line:
           q = int(line[19])
           temp["Interest"] = q
       elif "Pred" in line:
           temp["Pred"] = line[7:] 
           reject.append(temp)
           temp = {}

l = []
temp = {} 
old = -1
tl = []
for line in reject:
    if old != line["index"]:
        if temp:
           temp["reject"] = tl
           l.append(temp)
        temp = {} 
        tl = []
        temp["index"] = line["index"]
    if "false" in line["Pred"]: 
        tl.append(line["Interest"])
    old = line["index"]

if temp:
    temp["reject"] = tl
    l.append(temp)

reject = []
for elem in l:
    reject.append(elem["reject"]) 
        
with open("reject.json", "w") as f:
   json.dump(reject, f)



