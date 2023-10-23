import sys
import os
import json
from datetime import datetime

program_path = "/home/se/Dokumenty/WayApp_konsola"
communication_mode = "text"
path_character="/"

class System:
    #tests
    def test():
        print("test")

    #data.json
    def get_data():
        file = open(program_path + "{character}data{character}data.json".format(character=path_character), "r")
        file_text = file.read()
        file.close()
        data_json = json.loads(file_text)
        return data_json
    def update_data(data_type, value):
        system_data = System.get_data()
        system_data[data_type] = value
        file = open(program_path + "{character}data{character}data.json".format(character=path_character), "w")
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
    def check_data_files():
        if not os.path.exists(program_path):
            print("Błąd ścieżki programu1")
            sys.exit("Error")
        System.check_directory(program_path + "{character}data".format(character=path_character))
        add_file(program_path + "{character}data{character}data.json".format(character=path_character), { "last_project_id": 0, "last_task_id": 0 })
    def fix_project(id):
        if not os.path.exists(program_path):
            print("Błąd ścieżki programu")
        
        project_directory = program_path + "{character}data{character}".format(character=path_character) + System.formatid(int(id))

        project_default = json.dumps({ "name": "Project", "tasks": [], "tags": [] })
        default_values = {"name": "", "tasks": [], "tags": []}
        if not os.path.exists(project_directory + "{character}info.json".format(character=path_character)):
            write(project_directory + "{character}info.json".format(character=path_character), project_default)
        
        try:
            project_data = json.loads(System.read_file(project_directory + "{character}info.json".format(character=path_character)))
        except:
            write(project_directory + "{character}info.json".format(character=path_characters), project_default)
        
        project_data = json.loads(System.read_file(project_directory + "{character}info.json".format(character=path_character)))

        for element in ["name", "tasks", "tags"]:
            try:
                test = project_data[element]
            except:
                project_data[element] = default_values[element]
                write(project_directory + "{character}info.json".format(character=path_character), json.dumps(project_data))

class Communication:
    def print(title, list=[], levels=2):
        if (communication_mode == "json"):
            print(json.dumps({"title": title, "list": list}))
        else:
            print(title)
            for element in list:
                line = ""
                if(levels == 2):
                    for element2 in element:
                        line += element2 + " "
                else:
                    line = element + " "
                line = line[:-1]
                print(line)

class Project:
    def __init__(self, name):
        self.name = name
        self.tasks = []
        self.tags = []
        self.saved = False
    def find(self, id):
        self.directory = program_path + "{character}data{character}".format(character=path_character) + System.formatid(int(id))
        project_data = json.loads(read(self.directory + "{character}info.json".format(character=path_character)))
        self.name = project_data['name']
        self.tasks = project_data['tasks'] or []
        self.tags = project_data['tags']
        self.id = id
        self.saved = True
    def get_all(search = ""):
        all_projects_list = []
        last_project_id = System.get_data()["last_project_id"]
        for i in range(1, last_project_id+1):
            project_directory = program_path + "{character}data{character}".format(character=path_character) + System.formatid(i)
            if os.path.exists(project_directory):
                project_data = json.loads(read(project_directory + "{character}info.json".format(character=path_character)))
                project_data["id"] = i
                if(search == "" or (search in project_data["tags"])):
                    all_projects_list.append(project_data)
        return all_projects_list
    def save(self):
        if(not self.saved):
            self.id = System.get_data()["last_project_id"]+1
            self.directory = program_path + "{character}data{character}".format(character=path_character)+System.formatid(self.id)
            System.check_directory(self.directory)
        
        write(self.directory+"{character}info.json".format(character=path_character), json.dumps({ "name": self.name, "tasks": self.tasks, "tags": self.tags }))

        if(not self.saved):
            System.update_data("last_project_id", self.id)
    def add_tag(self, tag_name):
        self.tags.append(tag_name)
        self.save()
    def delete_tag(self, tag_name):
        self.tags.remove(tag_name)
        self.save()
    def get_project(self):
        project_data = json.loads(read(self.directory + "/info.json"))
        project_data["id"] = self.id
        return project_data
                
class Task:
    def __init__(self, project_id, name, date=""):
        self.project_id = project_id
        self.name = name
        self.date = date
        self.saved = False
    def project_tasks(project_id):
        project = Project("")
        project.find(project_id)
        return project.tasks
    def get_all(search = ""):
        all_tasks_list = []
        last_project_id = System.get_data()["last_project_id"]
        for i in range(1, last_project_id+1):
            project = Project("")
            project.find(i)
            project.id = i
            for task in project.tasks:
                task["project_id"] = i
                if(search == "" or search in task["name"]):
                    all_tasks_list.append(task)
            
            #project_directory = program_path + "{character}data{character}" + System.formatid(i)
            #if os.path.exists(project_directory):
            #    project_data = json.loads(read(project_directory + "{character}info.json"))
            #    project_data["id"] = i
            #    for task in project_data["tasks"]:
            #        task["project_id"] = i
            #        if(search == "" or search in task["name"]):
            #            all_tasks_list.append(task)
            
        return all_tasks_list
    def save(self):
        project = Project("")
        project.find(self.project_id)
        if(not self.saved):
            self.id = System.get_data()["last_task_id"] + 1
            project.tasks.append({"id": self.id, "name": self.name, "date": self.date})
        
        #write(self.directory+"{character}info.json", json.dumps({ "name": self.name, "tasks": self.tasks, "tags": self.tags }))

        if(self.saved == True):
            for task in project["tasks"]:
                if(task["id"] == self.id):
                    task["name"] = self.name
                    task["date"] = self.date
        
        project.save()

        if(not self.saved):
            System.update_data("last_task_id", self.id)

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
System.check_data_files()
for project in Project.get_all():
    System.fix_project(project["id"])

#Data from files
data = json.loads(read(program_path + "{character}data{character}data.json".format(character=path_character)))

#Commands

if len(sys.argv) < 2:
    commands_list = ["list",
                     "new_project nazwa",
                     "add_task projekt zadanie",
                     "all_tasks_list",
                     "task_list projekt",
                     "show_project projekt",
                     "add_tag projekt tag",
                     "delete_tag projekt tag",
                     "search_in_projects projektid tag",
                     "open_project projektid"]
    Communication.print("Komendy", commands_list, 1)
    #print("Dostępne komendy: ")
    #print("list")
    #print("new_project nazwa")
    #print("add_task projekt zadanie")
    #print("all_tasks_list")
    #print("task_list projekt")
    #print("show_project projekt")
    #print("add_tag projekt tag")
    #print("delete_tag projekt tag")
    #print("search_in_projects projektid tag")
    #print("open_project projektid")
elif sys.argv[1] == "list": #list of projects
    print_text = []
    all_projects_list = Project.get_all()
    for project in all_projects_list:
        print_text.append([System.formatid(project["id"]), project["name"]])
    Communication.print("Projects:", print_text, 2)
elif sys.argv[1] == "new_project": #new project
    project = Project(sys.argv[2])
    project.save()
    Communication.print("Created project " + project.name, [], 1)
elif sys.argv[1] == "add_task":
    task_project_id = sys.argv[2]
    task_name = sys.argv[3]
    task_date = sys.argv[4]

    task = Task(task_project_id, task_name, task_date)
    task.save()

    #project_directory = program_path + "{character}data{character}" + System.formatid(int(task_project_id))
    #project_data = json.loads(read(project_directory + "{character}info.json"))
    #try:
    #    project_data["tasks"].append({"id": data["last_task_id"]+1, "name": task_name, "date": task_date})
    #except:
    #    project_data.append({"tasks": []})
    #    print("Dodano")
    #    project_data["tasks"].append({"id": data["last_task_id"]+1, "name": task_name, "date": task_date})
    #write(project_directory + "{character}info.json", json.dumps(project_data))
    #data["last_task_id"]+=1

    #write(program_path + "{character}data{character}data.json", json.dumps(data))
    Communication.print("Dodano zadanie", [], 1)
elif sys.argv[1] == "all_tasks_list":
    print_text = []
    all_tasks = Task.get_all()
    for task in all_tasks:
        try:
            task_date = task["date"]
        except:
            task_date = "brak daty"
        project = Project("")
        project.find(int(task["project_id"]))
        print_text.append([task["name"], "  (" +project.name + ", " + task_date + ")"])
        #print(task["name"] + chr(9)+ "  (" +project.name + ", " + task_date + ")")

    #for i in range(1, data["last_project_id"]+1):
    #    project_directory = program_path + "{character}data{character}" + System.formatid(i)
    #    project_id = System.formatid(i)
    #    if os.path.exists(project_directory):
    #        try:
    #            project_data = json.loads(read(project_directory + "{character}info.json"))
    #            test = project_data["tasks"]
    #        except:
    #            project_data = json.loads(read(project_directory + "{character}info.json"))
    #            project_data["tasks"] = []
    #            write(project_directory + "{character}info.json", json.dumps(project_data))
    #        for task in project_data["tasks"]:
    #            try:
    #                task_date = task["date"]
    #            except:
    #                task_date = "brak daty"
    #            print(task["name"] + chr(9) +  "  (" + project_data["name"] + ", " + task_date + ")")
    Communication.print("All tasks list:", print_text, 2)
            
elif sys.argv[1] == "task_list":
    print_text = []
    project_id = sys.argv[2]
    tasks = Task.project_tasks(project_id)
    for task in tasks:
        print_text.append([str(task["id"]), task["name"], " (" + task["date"] + ")"])
    Communication.print("Tasks " + str(project_id), print_text, 2)
elif sys.argv[1] == "show_project":
    print_text = []
    project = Project("")
    project.find(int(sys.argv[2]))
    print_text.append(["name:", project.name])
    print_text.append(["tasks:", str(project.tasks)])
    print_text.append(["tags:", str(project.tags)])
    print_text.append(["id:", str(project.id)])
    Communication.print("Show project", print_text, 2)
elif sys.argv[1] == "add_tag":
    project = Project("")
    project.find(int(sys.argv[2]))
    project.add_tag(sys.argv[3])
    Communication.print("Tag added successfully!", [], 1)
elif sys.argv[1] == "delete_tag":
    project = Project("")
    project.find(int(sys.argv[2]))
    project.delete_tag(sys.argv[3])
    Communication.print("Tag " + sys.argv[3] + " deleted.", [], 1)
elif sys.argv[1] == "search_in_projects":
    print_text = []
    all_projects_list = Project.get_all(sys.argv[2])
    for project in all_projects_list:
        print_text.append([System.formatid(project["id"]), project["name"]])
    Communication.print("Searching results", print_text, 2)
elif sys.argv[1] == "open_project":
    path = program_path +  "{character}data{character}".format(character=path_character) + System.formatid(int(sys.argv[2]))
    try:
        os.startfile(path)
    except:
        os.system("open " + path)
