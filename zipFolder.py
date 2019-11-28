from shutil import make_archive


def zipFolder(folderName):
    """
    Creates a .zip folder of a given directory given a path to a folder.
    The outputted .zip will be in the same directory as the parent of
    the target folder.
    """

    make_archive(folderName, 'zip', folderName)
