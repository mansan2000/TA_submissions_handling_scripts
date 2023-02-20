import zipfile
import os
import shutil
import sys


'''
Script to get all neccasary files with a specified extension from the downloaded submissions from canvas and put
them in folders titled with students first and last name. This program asks for two students names and gets only the students between them
to make it easy to grade assignments and just get the students you need.

'''



# Function to get the directory that this script resides in to use as cwd
def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))
cwd = get_script_path()

print("\n\nTo run this script make sure that the extracted folder of submissions is in the same directory as this script and appended with the the assigment it is for (eg. hw01, lab01...\n")
assignment = input("Enter in assignment (eg. hw01, lab01)")
startStudentnum = input("Enter starting student whole name in format lastnamefirstname: ")
endStudentnum = input("Enter ending student whole name in format lastnamefirstname: ")

extensionLookingFor = input("enter in extension you want to get files for")
# Set up our folders to work from our current working directory 
fromFolder = cwd+"/"+"submissions"+assignment
extractedFolder = cwd+"/"+"submissionsExtracted"+assignment
outFolder = cwd+"/"+assignment+"Files"

# print(cwd)
# If output files have already been generated then delete them and their contents
try:
    shutil.rmtree(outFolder)
    shutil.rmtree(extractedFolder)
except:
    print("Generating New Files")

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
   for root, dirs, files in os.walk(filepath,followlinks=True):
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
            # print(folder)
            studentName = folder.split("_", 1)[0] #get student name
            try:
                with zipfile.ZipFile(fromFolder+"/"+folder, "r") as zip_ref:
                    zip_ref.extractall(extractedFolder+"/"+studentName+"/")
            except:
                print("Bad zip: "+studentName)
        elif folder.endswith(extensionLookingFor):
            studentName = folder.split("_", 1)[0] #get student name
            try:
                os.mkdir(extractedFolder+"/"+studentName)
            except Exception:
                pass


            # # print(folder)
            # print(studentName)
            # print(extractedFolder+"/"+studentName+"/"+folder)
            shutil.copy2(fromFolder+"/"+folder, extractedFolder+"/"+studentName+"/"+folder)

'''
Function that finds the java files in each student folder in our extractedFolder and copies them to our output folder and prepends the students name on the file name 
'''
def copyFiles():
    files = list_files(extractedFolder, ".java")
    TF = False
    for file in files:
        if startStudentnum in file:
            TF = True
        if TF:
            if file.endswith(extensionLookingFor) and file.find("MACOSX") == -1:
                extractedFolderPlus = extractedFolder +"\\"
                start = file.find(extractedFolderPlus) + len(extractedFolderPlus)
                end = file.find("\\", start)
                nameOfStudent = file[start:end]
                nameOfFile = file.rsplit("\\", 1)[1]
                try:
                    os.mkdir(outFolder+"/"+nameOfStudent)
                except Exception:
                    pass
                shutil.copy2(file, outFolder+"/"+nameOfStudent+"/"+nameOfFile)
        if endStudentnum in file:
            TF = False

unzipFiles()
copyFiles()
