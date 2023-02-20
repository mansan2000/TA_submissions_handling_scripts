import zipfile
import os
import shutil
import sys
import time

# Function to get the directory that this script resides in to use as cwd
def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))
cwd = get_script_path()

assignment = "lab02"
extensionLookingFor = ".java"
# Set up our folders to work from our current working directory 
fromFolder = cwd+"/"+"submissions"+assignment
extractedFolder = cwd+"/"+"submissionsExtracted"+assignment
outFolder = cwd+"/"+assignment+"FilesMOSS"

# print(cwd)
# If output files have already been generated then delete them and their contents
try:
    shutil.rmtree(outFolder)
    shutil.rmtree(extractedFolder)
except:
    pass

os.makedirs(extractedFolder) # create folder for unziped files
os.makedirs(outFolder) #create output folder
# cwd = os.getcwd() #find current working directory 


'''
Function that finds the paths to all the files in a given folder with a certian extension and returns the paths
Params: 
    filepath: path to folder to search
    filetype: file extension that we want to search for 
'''
def list_files(filepath, filetype):
   paths = []
   for root, dirs, files in os.walk(filepath):
      for file in files:
         if file.lower().endswith(filetype.lower()):
            paths.append(os.path.join(root, file))
   return(paths)


'''
Function that unzips all the files in the submission folder and puts them in the extractedFolder sorted into folders by student name
'''
def unzipFiles():
    for folder in os.listdir(fromFolder):
        if folder.endswith(".zip"):
            studentName = folder.split("_", 1)[0] #get student name
            try:
                with zipfile.ZipFile(fromFolder+"/"+folder, "r") as zip_ref:
                    zip_ref.extractall(extractedFolder+"/"+studentName+"/")
            except:
                print("Bad zip: "+studentName)


'''
Function that finds the java files in each student folder in our extractedFolder and copies them to our output folder and prepends the students name on the file name 
'''
def copyFiles():
    files = list_files(extractedFolder, ".java")
    for file in files:
        if file.endswith(extensionLookingFor) and file.find("MACOSX") == -1:
            extractedFolderPlus = extractedFolder +"\\"
            start = file.find(extractedFolderPlus) + len(extractedFolderPlus)
            end = file.find("\\", start)
            nameOfStudent = file[start:end]
            nameOfFile = file.rsplit("\\", 1)[1]
            shutil.copy2(file, outFolder+"/"+nameOfStudent+"_"+nameOfFile)


unzipFiles()
copyFiles()