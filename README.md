# Smart Security Camera

## About
The Smart Security Camera is a physical tool written in Python using OpenCV.
It is meant to provide similar video and image surveillance services offered by traditional security systems while minimizing
storage space and taking advantage of computer vision technologies.

## How to Run
### Dependencies
You will need a system that has a camera and Python 3.x installed, along with the numpy and OpenCV libraries. 
Further, OpenCV requires an additional contributions library to get the facial recognition working. This can be installed using pip
like:
<code> pip install opencv-contrib-python </code>

### Setup
Once you have all of the dependencies, you simply need to download the files in this repository.
Smart Security Camera uses a email to send a certain email address surveillance data once per day.
In the config.py file, enter the following information
* **fromAlias** This is from whom a recipient's inbox will say each daily report is from. You can leave it to the default "Smart Security Program" if you wish.
* **fromAddr** This is the email address from which the camera will send daily reports. You must change this to an email address that exists and you own. Gmail addresses work best.
* **fromPass** This is the password to the email account that the security camera will use to send daily reports. You much change this to be the password for the email entered in the fromAddr field.
* **toAddr** This is the email address to which the camera will send daily reports. You much change this to an email address that exists.
* **toAlias** This is the nickname that the camera will call the recipient of daily reports. You can leave it to the default "Camera User" if you wish.

### Execution
Once you have installed all dependiencies and performed the setup, you are ready to run.
Simply run the run.py file the same way you would run any other Python script.
In Linux, this would be done in the terminal as
<code> python3 run.py </code>

### Possible Issues
* **My camera isn't sending emails.** First try using a Gmail account for the camera to send reports. This account must have [two-factor authenication (2FA) turned off](https://myaccount.google.com/security), and must [allow less secure apps](https://myaccount.google.com/lesssecureapps?pli=1).
