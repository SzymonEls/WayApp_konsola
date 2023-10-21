import sys
import os
import json
from datetime import datetime

program_path = "C:\\Users\\Szymon\\Desktop\\WayApp_konsola"

class System:
    #tests
    def test():
        print("test")

    #data.json
    def get_data():
        file = open(program_path + "\\data\\data.json", "r")
        file_text = file.read()
        file.close()
        data_json = json.loads(file_text)
        return data_json
    def update_data(data_type, value):
        system_data = System.get_data()
        system_data[data_type] = value
        file = open(program_path + "\\data\\data.json", "w")
        file.write(json.dumps(system_data))
        file.close()

    #file format
    def formatid(number):
        return str("{:03d}".format(number))
    
    #files
    def write_file(directory, text):
        file = open(directory, "w")
        file.write(text)
        file.close()
    def read_file(directory):
        f = open(directory, "r")
        r = f.read()
        f.close()
        return r
    def check_directory(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    #fix
    def fix_project(id):
        if not os.path.exists(program_path):
            print("Błąd ścieżki programu")
        
        project_directory = program_path + "\\data\\" + System.formatid(int(id))

        project_default = json.dumps({ "name": "Project", "tasks": [], "tags": [] })
        default_values = {"name": "", "tasks": [], "tags": []}
        if not os.path.exists(project_directory + "\\info.json"):
            write(project_directory + "\\info.json", project_default)
        
        try:
            project_data = json.loads(System.read_file(project_directory + "\\info.json"))
        except:
            write(project_directory + "\\info.json", project_default)
        
        project_data = json.loads(System.read_file(project_directory + "\\info.json"))

        for element in ["name", "tasks", "tags"]:
            try:
                test = project_data[element]
            except:
                project_data[element] = default_values[element]
                write(project_directory + "\\info.json", json.dumps(project_data))

        

class Project:
    def __init__(self, name):
        self.name = name
        self.tasks = []
        self.tags = []
        self.saved = False
    def find(self, id):
        self.directory = program_path + "\\data\\" + System.formatid(int(id))
        project_data = json.loads(read(self.directory + "\\info.json"))
        self.name = project_data['name']
        self.tasks = project_data['tasks'] or []
        self.tags = project_data['tags']
        self.id = id
        self.saved = True
    def get_all(search = ""):
        all_projects_list = []
        last_project_id = System.get_data()["last_project_id"]
        for i in range(1, last_project_id+1):
            project_directory = program_path + "\\data\\" + System.formatid(i)
            if os.path.exists(project_directory):
                project_data = json.loads(read(project_directory + "\\info.json"))
                project_data["id"] = i
                if(search == "" or (search in project_data["tags"])):
                    all_projects_list.append(project_data)
        return all_projects_list
    def save(self):
        if(not self.saved):
            self.id = System.get_data()["last_project_id"]+1
            self.directory = program_path + "\\data\\"+System.formatid(self.id)
            System.check_directory(self.directory)
        
        write(self.directory+"\\info.json", json.dumps({ "name": self.name, "tasks": self.tasks, "tags": self.tags }))

        if(not self.saved):
            System.update_data("last_project_id", self.id)
    def add_tag(self, tag_name):
        self.tags.append(tag_name)
        self.save()
    def delete_tag(self, tag_name):
        self.tags.remove(tag_name)
        self.save()
    def get_project(self):
        project_data = json.loads(read(project_directory + "/info.json"))
        project_data["id"] = self.id
        return project_data
                
class Task:
    def __init__(self, project_id, name, date=""):
        self.project_id = project_id
        self.name = name
        self.date = date
        self.saved = False
    def get_all(search = ""):
        all_tasks_list = []
        last_project_id = System.get_data()["last_project_id"]
        for i in range(1, last_project_id+1):
            project_directory = program_path + "\\data\\" + System.formatid(i)
            if os.path.exists(project_directory):
                project_data = json.loads(read(project_directory + "\\info.json"))
                project_data["id"] = i
                for task in project_data["tasks"]:
                    if(search == "" or search in task["name"]):
                        all_tasks_list.append(task)
            return all_tasks_list
    def save(self):
        project = Project("")
        project.find(self.project_id)
        if(not self.saved):
            self.id = System.get_data()["last_task_id"] + 1
            project["tasks"].append(json.dumps({"id": self.id, "name": self.name, "date": self.date}))
        
        #write(self.directory+"\\info.json", json.dumps({ "name": self.name, "tasks": self.tasks, "tags": self.tags }))

        if(self.saved == True):
            for task in project["tasks"]:
                if(task["id"] == self.id):
                    task["name"] = self.name
                    task["date"] = self.date
        
        project.save()

        if(not self.saved):
            System.update_data("last_project_id", self.id)

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

# Check files
System.fix_project(1)
check_directory(program_path + "\\data")
add_file(program_path + "\\data\\data.json", { "last_project_id": 0, "last_task_id": 0 })

for project in Project.get_all():
    System.fix_project(project["id"])

#Data from files
data = json.loads(read(program_path + "\\data\\data.json"))

#Commands

if len(sys.argv) < 2:
    print("Dostępne komendy: ")
    print("list")
    print("new_project nazwa")
    print("add_task projekt zadanie")
    print("all_tasks_list")
    print("task_list projekt")
    print("show_project projekt")
    print("add_tag projekt tag")
    print("delete_tag projekt tag")
    print("search_in_projects projektid tag")
    print("open_project projektid")
elif sys.argv[1] == "list": #list of projects
    print("lista projektów: ")
    all_projects_list = Project.get_all()
    for project in all_projects_list:
        print(System.formatid(project["id"]) + chr(9)+project["name"])
elif sys.argv[1] == "new_project": #new project
    project = Project(sys.argv[2])
    project.save()
    print("Created project "+project.name)
elif sys.argv[1] == "add_task":
    task_project_id = sys.argv[2]
    task_name = sys.argv[3]
    task_date = sys.argv[4]

    task = Task(task_project_id, task_name, task_date)
    task.save()

    #project_directory = program_path + "\\data\\" + System.formatid(int(task_project_id))
    #project_data = json.loads(read(project_directory + "\\info.json"))
    #try:
    #    project_data["tasks"].append({"id": data["last_task_id"]+1, "name": task_name, "date": task_date})
    #except:
    #    project_data.append({"tasks": []})
    #    print("Dodano")
    #    project_data["tasks"].append({"id": data["last_task_id"]+1, "name": task_name, "date": task_date})
    #write(project_directory + "\\info.json", json.dumps(project_data))
    #data["last_task_id"]+=1

    #write(program_path + "\\data\\data.json", json.dumps(data))
    print("Dodano zadanie")
elif sys.argv[1] == "all_tasks_list":
    for i in range(1, data["last_project_id"]+1):
        project_directory = program_path + "\\data\\" + System.formatid(i)
        project_id = System.formatid(i)
        if os.path.exists(project_directory):
            try:
                project_data = json.loads(read(project_directory + "\\info.json"))
                test = project_data["tasks"]
            except:
                project_data = json.loads(read(project_directory + "\\info.json"))
                project_data["tasks"] = []
                write(project_directory + "\\info.json", json.dumps(project_data))
            for task in project_data["tasks"]:
                try:
                    task_date = task["date"]
                except:
                    task_date = "brak daty"
                print(task["name"] + chr(9) +  "  (" + project_data["name"] + ", " + task_date + ")")
            
elif sys.argv[1] == "task_list":
    project_id = sys.argv[2]
    project_directory = program_path + "\\data\\" + System.formatid(int(project_id))
    try:
        if os.path.exists(project_directory):
            project_data = json.loads(read(project_directory + "\\info.json"))
            print("Zadania projektu " + project_data["name"])
            for task in project_data["tasks"]:
                print(str(task["id"]) + " " + task["name"])
    except:
        print("BRAK ZADAŃ")
elif sys.argv[1] == "show_project":
    project = Project("")
    project.find(int(sys.argv[2]))
    print("name " + project.name)
    print("tasks " + str(project.tasks))
    print("tags " + str(project.tags))
    print("id " + str(project.id))
elif sys.argv[1] == "add_tag":
    project = Project("")
    project.find(int(sys.argv[2]))
    project.add_tag(sys.argv[3])
    print("Tag added successfully!")
elif sys.argv[1] == "delete_tag":
    project = Project("")
    project.find(int(sys.argv[2]))
    project.delete_tag(sys.argv[3])
    print("Tag " + sys.argv[3] + " deleted.")
elif sys.argv[1] == "search_in_projects":
    all_projects_list = Project.get_all(sys.argv[2])
    for project in all_projects_list:
        print(System.formatid(project["id"]) + chr(9)+project["name"])
elif sys.argv[1] == "open_project":
    path = program_path +  "\\data\\" + System.formatid(int(sys.argv[2]))
    os.startfile(path)