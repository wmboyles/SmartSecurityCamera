from SecurityRunner import runDay
from time import strftime, localtime
from sendMail import sendMail
from shutil import rmtree
from os import listdir

fromAlias  = "Smart Security Program"
fromAddr   = "myCamera@gmail.com" #not a real address. Use an existing account
fromPW     = "A MAIL PASSWORD" #Password for account you use
subject    = ""
message    = ""
folderList = []

def runAllDays(toAddr, toAlias="User"):
    """
    Calls a function that runs the security camera funtion once per day.
    This function will automatically exit once the day has changed, or if
    a user hit the ESC key.

    In both cases, a folder containing items corresponding to the finished day
    will be zipped into a folder, and sent using provided sender and recipient
    account information. After this onformation is sent successfully, the images
    will be deleted locally to save storage space.

    If the user did not exit using the ESC key, the program will then restart the
    daily camera function. Otherwise, the program will exit.
    """
    
    exit_status = 0
    while exit_status == 0:
        #Create today's loop
        today = localtime()

        #Find out if today's program exited due to hitting ESC (-1) or day change (0)
        exit_status = runDay(today) #This function runs until the day changes

        #Attach the day's images and video and send an email
        folderName = strftime("Faces/%d-%m-%y")
        folderList = [folderName]
        subject = strftime("Report for %d-%m-%y", today)

        #Create a simple message
        numItems = len(listdir(folderName))
        message = """Hi {0},\n
Here is today's Smart Security Camera Report of {1} photos and {2} video.\n
I'll keep a lookout for you!\n
\n
-{3}""".format(toAlias,numItems-1,1, fromAlias)
        
        messageSent = sendMail(
            fromAlias,  # From alias
            fromAddr,   # From address
            fromPW,     # Sender password
            toAddr,     # To address
            subject,    # Subject
            message,    # Message Body
            [],         # List of files to attach
            folderList  # Folder to attach
        )

        # Delete the day's output if the message correctly sent. The .zip folder is automatically deleted by sendMail
        if messageSent:
            rmtree(folderName)
            print("Removed sent image folder")

        #break loop if user hit esc
        if exit_status == -1: break

        


if __name__ == '__main__':
    runAllDays("recipient@email.com", "A. User") #recipient address, recipient nickname
