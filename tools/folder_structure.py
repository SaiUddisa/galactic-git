import subprocess
import os

def folder_structure(path,attempt):
    os.chdir(path)
    if attempt<1:
        p=subprocess.run(["git","checkout",os.getenv("BASE_BRANCH")])
        p0=subprocess.run(["git","pull"])
    
    p1 = subprocess.Popen(
        ["find", ".", "-maxdepth", "6", "-not", "-path", "*/.*"],
        
        stdout=subprocess.PIPE
    )

    p2 = subprocess.Popen(
        ["grep", "-vE", "node_modules|.git|dist|.next|public"],
        stdin=p1.stdout,
        stdout=subprocess.PIPE,
        text=True
    )

    
    p1.stdout.close()

    
    output, error = p2.communicate()
    return output
