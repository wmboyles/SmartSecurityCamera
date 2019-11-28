from shutil import make_archive


# Creates a zip folder of a folder in the same directory with the smae name.
def zipFolder(folderName):
    make_archive(folderName, 'zip', folderName)
