import shlex
import subprocess
import os
def fetch_code(commands,path):
    os.chdir(path)
    final_code=""   
    for command in commands:
        args = shlex.split(command)
        args.pop(0)
        args.pop(0)
        
        
        args.insert(0,"3")
        args.insert(0,"-HinrC")
        args.insert(0,"grep")
        
        p1 = subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        stdout,stderr = p1.communicate()
        if(stdout!=""):
            final_code+=stdout
    return(final_code)
        
