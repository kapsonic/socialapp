import requests
import json
import time
import datetime
import time
import sys
import os

class LiveEnsureApi:
    apiVersion = "5"
    stackLocation = "US"
    sessionToken = ""
    DEBUG = False

    def __init__(self, apiKey, apiPassword, agentId, host):
        self.apiKey = apiKey
        self.apiPassword = apiPassword
        self.agentId = agentId
        self.leHostBase = host
        self.leHostUrl = self.leHostBase + "/rest"

    def initSession(self, userId):
        data = {
            'apiVersion': self.apiVersion,
            'userId': userId,
            'agentId': self.agentId,
            'apiKey': self.apiKey
        }

        # logger("Starting session ... for " + userId)

        r = requests.put(self.leHostUrl + "/host/session", json=data)
        print(r.json())
        return r

    def addPromptChallenge(self, question, answer, sessionToken):
        type = "PROMPT"             # Required
        required = "true"           # Required
        fallback = "0"              # Required
        maxAt = "1"                 # Required

        details = {"question":question,
                   "answer":answer, 
                   "required":required, 
                   "fallbackChallengeID":fallback, 
                   "maximumAttempts":maxAt}
                
        data = {'sessionToken':str(sessionToken), 
                'challengeType':type, 
                'agentId':self.agentId, 
                'challengeDetails':details} 

        # logger("Adding prompt challenge ... ")

        c = requests.put(self.leHostUrl + "/host/challenge", json=data)

        # CHECKING STATUS CODE, PRINTING CHALLENGE

        return c

    def addTouchChallenge(self, orientation, touches, sessionToken):

        type = "HOST_BEHAVIOR"      # Required
        regionCount = "6"           # Grid pattern
        required = "true"           # Required
        fallback = "0"              # Required
        maxAt = "1"                 # Max retries

        details = {"orientation":orientation,
                   "touches":[1,2], 
                   "regionCount":regionCount,
                   "required":required, 
                   "fallbackChallengeID":fallback, 
                   "maximumAttempts":maxAt}
                
        data = {'sessionToken':str(sessionToken), 
                'challengeType':type, 
                'agentId':self.agentId, 
                'challengeDetails':details} 

        print(data)
        # logger("Adding a touch challenge ...")

        t = requests.put(self.leHostUrl + "/host/challenge", json=data)

        return t

    def addLocationChallenge(self, latitude, longitude, radius, sessionToken):

        type = "LAT_LONG"       # Required
        required = "true"       # Required
        fallback = "0"          # If fail, other challenge
        maxAt = "1"             # Retries

        details = {"latitude":latitude,
                   "longitude":longitude, 
                   "radius":radius,
                   "required":required, 
                   "fallbackChallengeID":fallback, 
                   "maximumAttempts":maxAt}
                
        data = {'sessionToken':str(sessionToken), 
                'challengeType':type, 
                'agentId':self.agentId, 
                'challengeDetails':details} 

        l = requests.put(self.leHostUrl + "/host/challenge", json=data)


        return l

    def getAuthObj(self, type, sessionToken):
        if sessionToken == "ERROR":
            # logger("Invalid SessionToken " + sessionToken)
            # logger("Quitting.")
            quit()

        qurl = self.leHostBase + "/QR?w=240&sessionToken=" + sessionToken
        furl = self.leHostBase + "/launcher?sessionToken=" + sessionToken
        lirl = self.leHostBase + "/launcher?sessionToken=" + sessionToken + "&light=1"
        lurl = "liveensure://?sessionToken=" + sessionToken +                                   "&status=" + self.leHostBase + "/rest"

        # logger("Returning " + type + " Auth Object")

        if type == "IMG":
            # logger(qurl)
            return(qurl)
        elif type == "COMBO":
            # logger(furl)
            return(furl)
        elif type == "LIGHT":
            # logger(lirl)
            return(lirl)
        elif type == "LINK":
            # logger(lurl)
            return(lurl)
        else:
            # logger("NO TOKEN")
            return "NOTOKEN"


    def pollStatus(self, sessionToken):
        if sessionToken == "ERROR":
            quit()

        p = requests.get(self.leHostUrl + "/host/session" + 
                    "/" + sessionToken + "/" + self.agentId)

        return p

    def deleteUser(self, userId):
        data = {
            'apiVersion': self.apiVersion,
            'userId': userId,
            'agentId': self.agentId,
            'apiKey': self.apiKey
        }

        d = requests.delete(self.leHostUrl + '/host/user', data=data)

        return d