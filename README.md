# SmartSecurityCamera

## About
The Smart Security Camera is a physical tool written in Python using OpenCV.
It is meant to provide similar video and image surveillance services offered by traditional security systems while minimizing
storage space and taking advantage of computer vision technologies.

## How to Run
### Dependencies
You will need a system that has a camera and Python 3.x installed, along with the numpy and OpenCV libraries. 
Further, OpenCV requires an additional contributions library to get the facial recognition working. This can be installed using pip
like:
<code>
pip install opencv-contrib-python
</code>

### Setup
Once you have all of the dependencies, you simply need to download the files in this repository.
Smart Security Camera uses a email to send a certain email address surveillance data once per day.
In the run.py file, enter in an email address and password in the fromAddr and fromPW fields. This is the account from which
Smart Security Camera will send emails. Next, at the very bottom of the run.py file, enter an email address and name.
This is the email address to which the Smart Security Camera will send data each day.

### Execution
Once you have installed all dependiencies and performed the setup, you are ready to run.
Simply run the run.py file the same way you would run any other Python script.
