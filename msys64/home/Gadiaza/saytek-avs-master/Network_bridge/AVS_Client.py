#!/usr/bin/env python3

import json
import pickle       #(incorrectly) used for encrypt and decrypt for now
#import subprocess
import os
from pathlib import PurePath
from secrets import base64  #for encrypt and decrypt

from Core.AVS_Misc_Utilities import waitForFile, waitForFileDeletion
import Core.AVSDB as AVSDB
import Core.AVSDBErrors as AVSDBErrors
import Core.AVSPrimitives as AVSPrimitives
#Investigate: Does importing these bloat the program (bc AVSDB also imports these)
from Network_bridge.ServerClient_Backends import JsonBackend

class ServerAVSBridge():
    def __init__(self, pcNum, serverFolder, backend, masterDB=None):
        self.pcNum = str(pcNum)
        self.serverFolder = PurePath(serverFolder)
        self.backend = backend
        self.masterDB = AVSDB.MasterDB(masterDB)        #client side for now (used for ui only)

    def newVoterBallot(self, name, grade, section):
        fileName = "voter" + self.pcNum + ".json"
        self.pushToServer(AVSDB.AVSPrimitives.Voter(name, grade, section), fileName, self.serverFolder)

        print("Requesting Ballot from server")
        waitForFileDeletion(PurePath(self.serverFolder, fileName))

        print("Awaiting Ballot from server")
        while True:
            try:
                error = self.pullFromServer("error" + self.pcNum + ".json", self.serverFolder, blocking=False)
            except FileNotFoundError:
                pass
            else:
                if not isinstance(error, AVSDBErrors.AVSError):
                    raise AVSDBErrors.InvalidDecodeRequestError

                raise error

            fileName = "clear_ballot" + self.pcNum + ".json"
            try:
                ballot = self.pullFromServer(fileName, self.serverFolder, blocking=False)
            except FileNotFoundError:
                continue
            else:
                if not isinstance(ballot, AVSPrimitives.Ballot):
                    raise AVSDBErrors.InvalidDecodeRequestError

                return ballot

    def processBallot(self, ballot):
        #print("Ballot: ", ballot)
        fileName = "ballot" + self.pcNum + ".json"
        self.pushToServer(ballot, fileName, self.serverFolder)

        print("Submitting ballot to server")
        while True:
            try:        #currently not in the original "spec"; just for safety; all of the stuff like this are expensive but are, in the end
                            #neglible bc this is supposed to block anyway and it will be changed to networking so yeah
                error = self.pullFromServer("error" + self.pcNum + ".json", self.serverFolder, blocking=False)
            except FileNotFoundError:
                pass
            else:
                if not isinstance(error, AVSDBErrors.AVSError):
                    raise AVSDBErrors.InvalidDecodeRequestError

                raise error

            try :
                confirmation = self.pullFromServer("vote_confirmation" + self.pcNum + ".json", self.serverFolder, blocking=False)
            except FileNotFoundError:
                continue
            else:
                break


        print("Ballot Submitted. Vote Incremented")

    def pushToServer(self, data, fileName, serverFolder, clientID=None):
        if clientID is None:        #should clientID even be parameterized?
            clientID = self.pcNum

        if not os.access(serverFolder, os.F_OK | os.R_OK | os.W_OK):    #Tests for the existence of the serverFolder and rw permissions
            raise AVSDBErrors.AVSServerConnectionError
        #data is first written to an intermediary file because the call to open()
        #creates an empty file, which is immediately taken in by the server,
        #effectively sending an invalid file (at least in the current implementation)
        #The intermediary data is written also directly into the serverFolder so that the file
        #will follow default permission rules in that server folder

        data = self.encrypt(self.backend.encode(data, {"clientID": clientID}))
        fil = open(PurePath(serverFolder, "." + fileName), "wb")
        fil.write(data)
        fil.close()
        os.replace(PurePath(serverFolder, "." + fileName), PurePath(serverFolder, fileName))

    def pullFromServer(self, fileName, serverFolder, delay=0.05, **kwargs):     #implement check if data_encoded["clientID"] == self.pcNum
        if not os.access(serverFolder, os.F_OK | os.R_OK | os.W_OK):    #Tests for the existence of the serverFolder and rw permissions
            raise AVSDBErrors.AVSServerConnectionError

        data_encoded = waitForFile(PurePath(serverFolder, fileName), mode="rb", delay=delay, **kwargs).read()    #why use wait for file?
        data = self.backend.decode(self.decrypt(data_encoded))
        os.remove(PurePath(serverFolder, fileName))

        return data

    #These are placeholder for now; no encryption used
    def encrypt(self, data):
        #base64 used here so that in case of a breach, the info of a voter as well as the candidates they voted for won't be in (practically) plain text
        #This does not make for any security, just false security through obscurity
        #TODO: Switch to a real encryption scheme
        try:
            return base64.encodebytes(pickle.dumps(data))
        except:
            raise AVSDBErrors.InvalidDecodeRequestError
    def decrypt(self, data):
        try:
            return pickle.loads(base64.decodebytes(data))
        except:
            raise AVSDBErrors.InvalidDecodeRequestError

    def ask_error_handling(self, error, voter):
        fileName =  "client_error{}.json".format(self.pcNum)
        self.pushToServer(error, fileName, self.serverFolder)
        data = self.pullFromServer("server_response{}.json".format(self.pcNum), self.serverFolder)
        ####Maybe check for data integrity here too?

        return data
