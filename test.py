import sys
import os
import json

directory = "data"
if not os.path.exists(directory):
    os.makedirs(directory)

if not os.path.isfile("data/data.json"):
    f = open("data/data.json", "w")
    data2 = {
        "last_id": 0
    }
    f.write(json.dumps(data2))
    f.close()

f = open("data/data.json", "r")
r = f.read()
data = json.loads(r)
f.close()


if sys.argv[1] == "list":
    print("lista projektów: ")
    print("a"+chr(9)+"b")
    print("ab"+chr(9)+"ccc")
elif sys.argv[1] == "new_project":
    project = {
        "name": sys.argv[2]
    }
    directory = "data/"+str("{:03d}".format(data["last_id"]+1))
    if not os.path.exists(directory):
        os.makedirs(directory)
    f = open(directory+"/info.json", "w")
    f.write(json.dumps(project))
    f.close()
    data["last_id"]+=1
    f = open("data/data.json", "w")
    f.write(json.dumps(data))
    f.close()
    print("Created project "+project["name"])
