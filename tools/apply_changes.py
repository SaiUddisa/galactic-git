import shlex
import subprocess
import os
def apply_changes(commands,path,branch_name):
    os.chdir(path)
    p1 = subprocess.Popen(["git","checkout","-b",branch_name])
    for command in commands:
        args = shlex.split(command)
        args.pop(0)
        args.insert(0,"sed")
        print(args)
        p1 = subprocess.Popen(args)
    
    return


