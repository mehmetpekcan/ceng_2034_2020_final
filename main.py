import os 
  
def fork_childProcess(): 
    # Fork a child process from parent process, it will be copy
    # of the parent process but in the identicial, they are different.
    childProcess = os.fork() 

    # childProcess greater than 0 means parent process 
    if childProcess > 0: print("Parent process and id is:", os.getpid()) 

    # childPorecess equals to 0 means child process 
    elif childProcess == 0: print("Child process and id is:", os.getpid()) 
          
# Driver code 
if __name__ == '__main__':
    fork_childProcess()