#
# Redunda-lib-Python
# Redunda.py
#
# Created by Ashish Ahuja (Fortunate-MAN) on 23rd July 2017.
#
#

from urllib import request, parse
import json
import pickle

class Redunda:
    def __init__ (self, key, filesToSync, version="unknown"):
        self.key = key
        self.filesToSync = filesToSync
        self.version = version
        self.location = "unknown"
        self.eventCount = 0
        self.shouldStandby = False

    def sendStatusPing (self):
        data = parse.urlencode({"key": self.key, "version": self.version}).encode()
        req = request.Request ("https://redunda.sobotics.org/status.json", data)

        response = request.urlopen (req)

        jsonReturned = json.loads (response.read().decode("utf-8"))

        self.location = jsonReturned ["location"]
        self.shouldStandby = jsonReturned ["should_standby"]
        self.eventCount = jsonReturned ["event_count"]

    def uploadFile (self, filename, ispickle=False):
        print ("Uploading file " + filename + " to Redunda.")
        
        url = "https://redunda.sobotics.org/bots/data/" + filename + "?key=" + self.key
        
        #Set the content type to 'application/octet-stream'
        header = {"Content-type": "application/octet-stream"}
        
        filedata = ""

        #Read the data from a file to a string.
        if filename.endswith (".pickle") or ispickle==True:
            dict = pickle.loads(filename)
            filedata = str (data)
        else:
            try:
                with open (filename, "r") as fileToRead:
                    filedata = fileToRead.read()
            except IOError as ioerr:
                print ("IOError occurred: " + str (ioerr))
                return

        requestToMake = request.Request (url, data=filedata.encode ("utf-8"), headers=header)

        #Make the request.
        response = request.urlopen (requestToMake)

        if response.code >= 400:
            print ("Error occurred while uploading file '" + filename + "' with error code " + str (response.code) + ".")

    def downloadFile (self, filename, ispickle=False):
        print ("Downloading file " + filename + " from Redunda.")

        url = "https://redunda.sobotics.org/bots/data/" + filename + "?key=" + self.key

        requestToMake = request.Request (url)

        #Make the request.
        response = request.urlopen (requestToMake)

        if response.code != 200:
            print ("Error occured while downloading file '" + filename + "' with error code '" + str (response.code) + ".")

        print (response.read().decode ("utf-8"))





