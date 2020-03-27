import smtplib  # mail server library

from os.path import basename
from os import remove

from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

from zipFolder import zipFolder



def sendMail(alias, fromAddr, pw, toaddr, subject="", message="", AttchFileList=[], AttchFolderList=[]):
    """
    Sends an email from a given certain gmail address given a password.
    Sender can be given any alias.
    Email is sent to a given mail address with an optioal subject and message body.
    Sender can optionally attach a list of file paths to be attached.
    Sender can also attach an entire directory as a zipFile by specifying a directory name.
    """
    
    msg = MIMEMultipart()  # create a message

    # setup the parameters of the message
    msg['From'] = alias + "<" + fromAddr + ">"  # FORMAT: "ALIAS <SEND ADDRESS>"
    msg['To'] = toaddr
    msg['Subject'] = subject
    
    # Add in the message body
    msg.attach(MIMEText(message, 'plain'))  # 'plain' or 'html'
    
    # add attachments as folders as a zip file
    for AttchFolder in AttchFolderList:
        zipFolder(AttchFolder)
        print("zipped " + AttchFolder)
        AttchFileList.append(AttchFolder + ".zip")

    # Attach Files from a list
    for AttchFile in AttchFileList:
        try:
            with open(AttchFile, "rb") as file:
                part = MIMEApplication(file.read(), Name=AttchFile)

            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(AttchFile)
            msg.attach(part)
            print("Attached " + AttchFile)
            
        except FileNotFoundError:
            if input(AttchFile + " not found. Send Anyways (Y/N)?").lower() != "y":
                print("Aborting Sending.")
                return False

    # remove zip files that we just created and attached
    for AttchFolder in AttchFolderList:
        remove(AttchFolder + ".zip")

    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()

    # Try to login to the mail service
    try:
        # do not turn on 2FA for this to work
        # may need to 'Allow less secure apps' at https://myaccount.google.com/lesssecureapps?pli=1
        s.login(fromAddr, pw)
    except smtplib.SMTPAuthenticationError:
        print("Invalid username or password. Aborting Sending.")
        return False
    
    # send the message via the server just set up.
    s.send_message(msg)
    del msg
        
    # Terminate the SMTP session and close the connection
    s.quit()

    print("Message Sent.")
    return True
