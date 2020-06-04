#*
#* Mehmet Pekcan
#* 170709038
#* For more detail check documentation:
#* https://mehmetpekcan.gitbook.io/ceng2034/
#*

import os
import requests 
import uuid
import re as regex
from hashlib import md5 
import time # to test elapsed times..
import multiprocessing
from itertools import product

#*
#* In the project there are two types of duplicate finder function
#* Difference between them is the way how they find, one of them 
#* finds using serial threading the other one finds using multiprocessing.
#* 
#* One more different is, the homework assignment was not clear 
#* do we find duplicate pair or just duplicate files? So i made
#* both of them.
#*

#*
#* To generate a hash to given image as a parameter
#*
def hashinize(image):
    with open(image, "rb") as imageFile:
        imageHash = md5(imageFile.read()).hexdigest()
    return imageHash

#*
#* If hash is unique means that there is no duplicate since
#* but if there is copy of hash in hashes objects, means that
#* there is duplicae append them to duplicates list to detect
#* 
def find_duplicates(imagesList):
    duplicates = []
    hashes = {}

    index = 0
    for image in imagesList:
        imageHash = hashinize(image)
        if(imageHash not in hashes):
            hashes[imageHash] = index
        else:
            duplicates.append((index, hashes[imageHash]))
        index += 1

    return duplicates

#*
#* h[0], hashes[0] => file hash number 
#* h[1], hashes[1] => file name
#*
def find_duplicates_by_multiproc(h, hashes):
    if h[0] == hashes[0]:
        return (h[1], hashes[1])


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
#* Just for printing out child process id
#*
def fork_childProcess_showID():
    childProcess = os.fork()
    if childProcess > 0:
        os.waitpid(childProcess, 0)
    elif childProcess == 0:
        print("Child process id is:", os.getpid())

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
        start = time.perf_counter()

        request_urls = [
                "http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg",
                "https://upload.wikimedia.org/wikipedia/tr/9/98/Mu%C4%9Fla_S%C4%B1tk%C4%B1_Ko%C3%A7man_%C3%9Cniversitesi_logo.png",
                "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg",
                "http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg",
                "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg"]
        
        # Downloading files
        [download_file(url) for url in request_urls]

        # Current working directory files
        cwdf = os.listdir()

        # Take only images for current working directory files
        cwdf = filter_files(cwdf)
        
        # To find duplicate files
        duplicates = find_duplicates(cwdf)


        end = time.perf_counter()
        print("Elapsed time with serial threading is: {}".format(round(end-start,2)))

        [print(i) for i in duplicates]

def fork_childProcess_by_multiproc():
    childProcess = os.fork() 

    if childProcess > 0:
        os.waitpid(childProcess, 0)

    elif childProcess == 0:
        start = time.perf_counter()

        processPool = multiprocessing.Pool()

        request_urls = [
                "http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg",
                "https://upload.wikimedia.org/wikipedia/tr/9/98/Mu%C4%9Fla_S%C4%B1tk%C4%B1_Ko%C3%A7man_%C3%9Cniversitesi_logo.png",
                "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg",
                "http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg",
                "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg"]

        processPool.map(download_file, request_urls)

        cwdf = os.listdir()
        cwdf = filter_files(cwdf)

        # List comphresion shorthand:
        # hashes = []
        # for h in cdwd:
        #   hashes.append(hashinize(h))
        hashes = [ (hashinize(h), h) for h in cwdf ]

        # Using buffered mapping function to determine which files duplicate        
        duplicateRaw = processPool.starmap(find_duplicates_by_multiproc, product(hashes, repeat=2) )

        # This is just for filtering to duplicate tuples from their duplicate :)
        duplicateFiltered = []
        for i in duplicateRaw:
            if i != None:
                if i[0] != i[1] and i[1]:
                    if i[0] not in duplicateFiltered:
                        duplicateFiltered.append(i[0])
                    elif i[1] not in duplicateFiltered:
                        duplicateFiltered.append(i[1])

        end = time.perf_counter()
        print(f"Elapsed time with multiprocessing is: {round(end-start,2)}\n")

        # Printing duplicate images...
        [print(i) for i in duplicateFiltered]

# Driver code 
if __name__ == '__main__':
    control = True
    while control:
        print("\nCommands:\n1 -> Create child process then show process id\n2 -> Download images then find duplicate ones\n3 -> Do second command using multiprocessing\n0 -> Quit")
        command = input()
        if command == "0":
            control = False
        elif command == "1":
            fork_childProcess_showID()
        elif command == "2":
            fork_childProcess()
        elif command == "3":
            fork_childProcess_by_multiproc()

