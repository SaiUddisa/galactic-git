import shlex
import subprocess
import os
def apply_changes(commands,path,branch_name,commit_message):
    os.chdir(path)
    p1 = subprocess.run(["git","checkout","-b",branch_name])
    for command in commands:
        args = shlex.split(command)
        args.pop(0)
        args.insert(0,"sed")
        print(args)
        p1 = subprocess.run(args)
    p2 = subprocess.run(["git" ,"add", "."])
    p3 = subprocess.run(["git" ,"commit", "-m",commit_message])
    p4 = subprocess.run(["git","push","origin",branch_name])
    return


