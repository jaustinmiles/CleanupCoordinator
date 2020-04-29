# Cleanup Coordinator
The cleanup coordinator is a custom cleanup task management system primarily for use in residential buildings. It
provides the abilities to assign tasks, send reminders, verify completion of tasks, and track progress toward 
various cleanup-oriented goals. The Cleanup Coordinator utilizes the Google Sheets, Twilio SMS, and AWS S3 APIs to
manage and manipulate data, along with the Flask python framework.

# Setup
In order to use the Cleanup Coordinator, you will need access to the Google Sheets and Twilio APIs, along with an AWS
instance of an S3 bucket. This data is provided to the Cleanup Coordinator through json files or through environment
variables, whichever is simpler. 

# Usage
To run the cleanup coordinator, simply clone the repository and run 
```
python app.py
```