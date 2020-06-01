import os
import requests 
import uuid
import re as regex
from hashlib import md5 


#*
#* Take whole images then open them as a file 
#* then read them after read, generate a unique 
#* hash then append  to returned list
#*
def hashinize(images):
    hashList  = []
    for image in images:
        with open(image, "rb") as image:
            hashList.append(md5(image.read()).hexdigest())
    return hashList

#*
#* Take a parameter as files then if files has
#* known types of image formats append them 
#* returned list, so you split images from
#* the other files
#*
def filter_files(files):
    formats = ["jpeg", "jpg", "png", "gif", "tiff", "eps", "svg", "pdf"]
    filtered_files = []

    for extension in formats:
        for file in files:
            if extension in file:
                filtered_files.append(file)
    return filtered_files

#*
#* To make well file name, find the image format
#* from the given links, if link has known types
#* of image formats, take that format then add 
#* to end of file_name
#*
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

#*
#* To download file, take url and optionally file name
#* then send get request to that url after fetching
#* response open a file then write response.content into
#* a file
#*
def download_file(url, file_name=None):
    file_name = find_image_format(url, file_name)
    response = requests.get(url, allow_redirects=True)
    open(file_name, "wb").write(response.content)


#*
#* Create child process which is duplicated from parent
#*
def fork_childProcess(): 
    # Fork a child process from parent process, it will be copy
    # of the parent process but in the identicial, they are different.
    childProcess = os.fork() 

    if childProcess > 0:
        # Wait for the process which has 0 pid
        os.waitpid(childProcess, 0)
    # childProcess equals 0 means child process otherwise it'll be parent process
    elif childProcess == 0:
        command = 1
        while(command != "0"):
            print("\n1 -> Show process id\n2 -> Download Images\n3 -> Find duplicate images\n0 -> Exit\n")
            command = input()
            if command == "1":
                print("Child process id is: {}\n".format(os.getpid())) 
            elif command == "2":
                request_urls = ["http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg",
    "https://upload.wikimedia.org/wikipedia/tr/9/98/Mu%C4%9Fla_S%C4%B1tk%C4%B1_Ko%C3%A7man_%C3%9Cniversitesi_logo.png",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg",
    "http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg"]
                for url in request_urls:
                    download_file(url)
            elif command == "3":
                # Current working directory files
                cwdf = os.listdir()

                # Take only images for current working directory files
                cwdf = filter_files(cwdf)

                # Generate hash for images
                hashList = hashinize(cwdf)

# Driver code 
if __name__ == '__main__':
    fork_childProcess()


