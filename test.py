import sys
import os
import json

def check_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def add_file(directory, o):
    if not os.path.isfile(directory):
        f = open(directory, "w")
        f.write(json.dumps(o))
        f.close()

def read(directory):
    f = open(directory, "r")
    r = f.read()
    f.close()
    return r

def write(directory, a):
    f = open(directory, "w")
    f.write(a)
    f.close()

def formatid(number):
    return str("{:03d}".format(number))


# Check files
check_directory("data")
add_file("data/data.json", { "last_id": 0 })

#Data from files
data = json.loads(read("data/data.json"))

#Commands

if sys.argv[1] == "list": #list of projects
    print("lista projektów: ")
    for i in range(1, data["last_id"]+1):
        project_directory = "data/" + formatid(i)
        project_id = formatid(i)
        if os.path.exists(project_directory):
            project_data = json.loads(read(project_directory + "/info.json"))
            print(project_id + chr(9)+project_data["name"])
elif sys.argv[1] == "new_project": #new project
    project = {
        "name": sys.argv[2],
        "tasks": []
    }
    directory = "data/"+formatid(data["last_id"]+1)
    check_directory(directory)

    write(directory+"/info.json", json.dumps(project))

    data["last_id"]+=1

    write("data/data.json", json.dumps(data))

    print("Created project "+project["name"])
elif sys.argv[1] == "add_task":
    task_project_id = sys.argv[2]
    task_name = sys.argv[3]
    project_directory = "data/" + formatid(int(task_project_id))
    project_data = json.loads(read(project_directory + "/info.json"))
    try:
        project_data["tasks"].append({"id": 1, "name": "a"})
    except:
        project_data.append({"tasks": []})
        print("Dodano")
        project_data["tasks"].append({"id": 1, "name": "a"})
    write(project_directory + "/info.json", json.dumps(project_data))
    
