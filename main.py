import os
import requests 
import uuid
import re as regex

def find_image_format(url, file_name):
    # if file has no parameter comes from user
    # generate an unique id
    file_name = file_name if file_name else str(uuid.uuid4())
    formats = ["jpeg", "jpg", "png", "gif", "tiff", "eps", "svg", "pdf"]

    # if any known files format has "url" find it
    # and suppose that this file is that format
    found_format = ""
    for extension in formats:
        for match in regex.finditer(extension, url):
            found_format = match.group()

    # return new file name with founded format of file
    return file_name+"."+found_format


def download_file(url, file_name=None):
    file_name = find_image_format(url, file_name)
    response = requests.get(url, allow_redirects=True)
    open(file_name, "wb").write(response.content)
    

def fork_childProcess(): 
    # Fork a child process from parent process, it will be copy
    # of the parent process but in the identicial, they are different.
    childProcess = os.fork() 

    # Basic CLI command for this app:
    # '1' for, seeing Child Process ID

    # childProcess equals 0 means child process otherwise it'll be parent process
    if childProcess > 0:
        print("Enter your command: ")
        command = input()
        if command == "1":
            print("Child process id is:", os.getpid()) 
        elif command == "2":
            request_urls = [
                "http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg",
                "https://upload.wikimedia.org/wikipedia/tr/9/98/Mu%C4%9Fla_S%C4%B1tk%C4%B1_Ko%C3%A7man_%C3%9Cniversitesi_logo.png",
                "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg​",
                "http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg​",
                "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg​"
            ]
            for url in request_urls:
                download_file(url)

# Driver code 
if __name__ == '__main__':
    fork_childProcess()