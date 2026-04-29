import shlex
import subprocess
import os
def apply_changes(commands,path,branch_name,commit_message):
    os.chdir(path)
    p1 = subprocess.run(["git","checkout","-b",branch_name])
    print("\n Creating Git Branch : "+branch_name)
    for command in commands:
        args = shlex.split(command)
        args.pop(0)
        args.insert(0,"sed")
        p1 = subprocess.run(args)
    p2 = subprocess.run(["git" ,"add", "."])
    print("\n Adding the Changes to Stage...\n")
    p3 = subprocess.run(["git" ,"commit", "-m",commit_message])
    print("\n Commit Message: "+commit_message)
    p4 = subprocess.run(["git","push","origin",branch_name])
    
    return


