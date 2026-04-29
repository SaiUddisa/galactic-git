import shlex
import subprocess
import os
def apply_changes(commands,path,branch_name,commit_message):
    os.chdir(path)
    p1 = subprocess.Popen(["git","checkout","-b",branch_name])
    for command in commands:
        args = shlex.split(command)
        args.pop(0)
        args.insert(0,"sed")
        print(args)
        p1 = subprocess.Popen(args)
    p2 = subprocess.Popen(["git" ,"add", "."])
    p3 = subprocess.Popen(["git" ,"commit", "-m",commit_message])
    p4 = subprocess.Popen(["git","push","origin",branch_name])
    return


