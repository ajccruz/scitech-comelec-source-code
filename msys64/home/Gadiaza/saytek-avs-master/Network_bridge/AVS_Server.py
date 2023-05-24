#!/usr/bin/env python3
#TODO: make all dump calls indent

import json
#import multiprocessing      #For AVSServerTUI
import os
import pickle       #used for encrypt() and decrypt() for now; will be used for encoding later
import subprocess
from pathlib import PurePath
from secrets import base64  #for encrypt and decrypt

from Core.AVS_Misc_Utilities import waitForFile
import Core.AVSDB as AVSDB   #For Main avs logic
import Core.AVSDBErrors as AVSDBErrors
import Core.AVSPrimitives as AVSPrimitives

class ClientAVSBridge():
    def __init__(self, mainAVS, maxPCNum, serverFolder, backend):     #incomplete
        self.mainAVS = mainAVS
        self.pcNums = [str(pcNum) for pcNum in range(1, maxPCNum + 1)]
        self.serverFolder = str(PurePath(serverFolder))        #sanitize before assignment? ( make sure it ends with /)
        self.localFolder = str(PurePath(".localFolder/"))       #unix hardcoded for now
        self.backend = backend
        self.exceptionDispatcher = AVSDB.AVSExceptionHandler()      #Hardcoded to a generic instance for now; this and AVSLogic.AVSexception_handler must have the same identifier for the adaptor model to work

    def startElection(self):
        #TODO: migrate these to the corresponding os calls
        #Make serverFolder a stickyFolder that only allows rwx for Owner(avsserver) and Group(avs)
        #The avs group is given permission so that clients can write to it for communication
        ####subprocess.run(["mkdir", "--mode", "1770", self.serverFolder])
        try:
            os.mkdir(self.serverFolder, mode=0o1770)
        except FileExistsError:
            print("WARNING: server folder existed before server even started. Starting the server with an unclean serverFolder might lead to problems (e.g. The unclean folder contains leftover data/files from a previous election.")
        os.chmod(self.serverFolder, 0o1770)     #chmod called here because sometimes permissions are lower than 1770, possibly because of umask, idk
        #Add special permissions for avsserver by default for each file created in the server folder so that avsserver can write replies to it
        subprocess.run(["setfacl", "-d", "-m", "u:avsserver:rwx", self.serverFolder])   ####No builtin way to set acl in python3
        #Make serverFolder a stickyFolder that only allows rwx for Owner(avsserver) and Group(avs)
        ####subprocess.run(["mkdir", "--mode", "1700", self.localFolder])
        try:
            os.mkdir(self.localFolder, mode=0o1700)
        except FileExistsError:
            pass

        os.chmod(self.localFolder, 0o1700)     #chmod called here because sometimes permissions are lower than 1770, possibly because of umask, idk
        for db in (self.mainAVS.votesDB, self.mainAVS.voterDB):      #maybe this step should be done avsdb? or in the top level gui?; masterDB not included for now as the ui also relies on that for info lookup, therefore needing read permission
            #subprocess.run(["chmod", "700", db.dbFile])     #a little unsafe as there's a lag between creation and stricter permissions, but meh
            os.chmod(db.dbFile, 0o700)
            #TODO: ake the avsserver as group scheme and turn on stgid bit
        #subprocess.run(["setfacl", "-dm", "o::---", self.serverFolder])

    def stopElection(self):
        ####Shutil is required to rm -R portably; will do it later
        subprocess.run(["rm", "-R", self.serverFolder])
        subprocess.run(["rm", "-R", self.localFolder])
        #print datetime of election end here
        print(AVSDB.datetime.datetime.now())
        #exit(0)

    def processNewVoters(self):
        for pcNum in self.pcNums:
            fileName = "voter" + pcNum + ".json"
            try:
                voter = self.pullFromServer(fileName, self.serverFolder, blocking=False)
            except FileNotFoundError:
                continue

            if not isinstance(voter, AVSPrimitives.Voter):
                raise AVSDBErrors.InvalidDecodeRequestError

            print("New voter from pc{}: {}".format(pcNum, voter))

            try:        #move to func?
                ballot = self.mainAVS.newVoterBallot(voter.name, voter.grade, voter.section)
            except AVSDBErrors.AVSDBError as error:
                self.handleError(error, pcNum)
            else:
                fileName = "clear_ballot{}.json".format(pcNum)
                self.pushToServer(ballot, fileName, self.serverFolder, clientID=pcNum)

    def processBallots(self):
        for pcNum in self.pcNums:
            fileName = "ballot" + pcNum + ".json"

            ballot = None
            try:
                ballot = self.pullFromServer(fileName, self.serverFolder, blocking=False)
            except FileNotFoundError:
                continue

            if not isinstance(ballot, AVSPrimitives.Ballot):
                raise AVSDBErrors.InvalidDecodeRequestError

            try:
                self.mainAVS.processBallot(ballot)
            except AVSDBErrors.AVSDBError as error:
                self.handleError(error, pcNum)
            else:
                fileName = "ballot{}.json".format(pcNum)
                ####os.remove(PurePath(self.serverFolder, fileName))
                self.pushToServer(None, "vote_confirmation{}.json".format(pcNum), self.serverFolder, clientID=pcNum)
            """ Needs to be rethought
            finally:
                prefixes = ["voter", "error", "clear_ballot", "client_error", "server_response"]#, "ballot"]
                for prefix in prefixes:
                    fileName = prefix + pcNum + ".json"
                    subprocess.getoutput(["rm %s" % self.serverFolder + fileName])      #getoutput() used so that messages are suppressed
            """

    def processErrors(self, ui_callback=None):        #Unfinished
        for pcNum in self.pcNums:
            fileName = "client_error{}.json".format(pcNum)
            try:
                error = self.pullFromServer(fileName, self.serverFolder, blocking=False)
            except FileNotFoundError:
                continue

            if not isinstance(error, AVSDBErrors.AVSError):
                raise AVSDBErrors.InvalidDecodeRequestError

            error.message = "(PC %s)" % pcNum + error.message   ####Hack to make the Server-side GUI show what pc number an error is from
            self.exceptionDispatcher.add_to_queue(error, error.voter, pcNum)
            #self.ask_error_handling(error, error.voter, ui_callback=ui_callback)

    def pushToServer(self, data, fileName, serverFolder, clientID=None):
        if not os.access(serverFolder, os.F_OK | os.R_OK | os.W_OK):    #Tests for the existence of the serverFolder and rw permissions
            raise AVSDBErrors.AVSServerUninitializedError

        #data is first written to an intermediary file because the call to open()
        #creates an empty file, which is immediately taken in by the server,
        #effectively sending an invalid file (at least in the current implementation)
        #The intermediary data is written also directly into the serverFolder so that the file
        #will follow default permission rules in that server folder

        data = self.encrypt(self.backend.encode(data, {"clientID": clientID}))
        fil = open(PurePath(self.localFolder, "server_acquired" + clientID), "wb")
        fil.write(data)
        fil.close()
        #subprocess.run(["mv", "{}server_acquired{}".format(self.localFolder, clientID), serverFolder + fileName])
        os.replace(PurePath(self.localFolder, "server_acquired" + clientID), PurePath(serverFolder, fileName))

    def pullFromServer(self, fileName, serverFolder,  delay=0.05, delete=True, **kwargs):
        if not os.access(serverFolder, os.F_OK | os.R_OK | os.W_OK):    #Tests for the existence of the serverFolder and rw permissions
            raise AVSDBErrors.AVSServerUninitializedError

        data_encoded = self.decrypt(waitForFile(PurePath(serverFolder, fileName), mode="rb", delay=delay, **kwargs).read())    #why use wait for file?
        data = self.backend.decode(data_encoded)
        if delete:
            clientID = data_encoded["clientID"]
            #subprocess.run(["mv", serverFolder + fileName, "{}server_acquired{}".format(self.localFolder, clientID)])
            os.replace(PurePath(serverFolder, fileName), PurePath(self.localFolder, "server_acquired" + clientID))
        return data

    def handleError(self, error, pcNum):
        encoded_error = self.backend.encodeError(error)

        fileName = "error" + str(pcNum) + ".json"
        self.pushToServer(error, fileName, self.serverFolder, clientID=pcNum)

    def encrypt(self, data):
        #base64 used here so that in case of a breach, the info of a voter as well as the candidates they voted for won't be in (practically) plain text
        #This does not make for any security, just false security through obscurity
        #TODO: Switch to a real encryption scheme
        try:
            return base64.encodebytes(pickle.dumps(data))
        except:
            raise AVSDBErrors.InvalidEncodeRequestError

    def decrypt(self, data):
        try:
            return pickle.loads(base64.decodebytes(data))
        except:
            raise AVSDBErrors.InvalidDecodeRequestError

    def ask_error_handling(self, error, voter, ui_callback=None):     #untested
        #if ui_callback == None:
            #ui_callback = mainServerQuery      ####Hardcoded for now

        data = self.mainAVS.ask_error_handling(error, voter, ui_callback)
        pcNum = self.exceptionDispatcher.allow_exception(error, voter)

        fileName = "server_response{}.json".format(pcNum)
        self.pushToServer(data ,fileName, self.serverFolder, clientID=pcNum)
