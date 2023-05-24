#!/usr/bin/env python3

import argparse

from Core.AVS_Misc_Utilities import getOfficeCandidates, parseMasterList, getConfig, getCandidates
import Core.AVSDB as AVSDB
import Core.AVSDBErrors as AVSDBErrors
from Network_bridge.ServerClient_Backends import JsonBackend
import Network_bridge.AVS_Server as AVS_Server

class AVSServerTUI():       #does not use any of the above
    def __init__(self, mainAVS):
        self.mainAVS = mainAVS

    def startElection(self):
        print("UI: Starting voting")
        self.mainAVS.startElection()
        while True:
            try:
                self.mainAVS.processNewVoters()
                self.mainAVS.processBallots()
                self.mainAVS.processErrors()    #Routine for picking up errors and queuing them
                for error in self.mainAVS.exceptionDispatcher.exception_stack:      #Actual loop that asks admin for next action
                    self.mainAVS.ask_error_handling(error["Exception"](), error["Voter"])
            except KeyboardInterrupt:   #Still ends process on "n"; fix later (tier10)
                if self.promptElectionEnd():
                    self.mainAVS.stopElection()     #abstract (i.e. make self.stopElection()) again?
                    #A stopElection() and self.mainProcess.terminate() is not needed for now
                    #bc mainAVS.stopElection() calls exit(0)
                    break

    def stopElection(self):
        self.mainAVS.stopElection()

    def promptElectionEnd(self):        #TUI oriented for now
        inpt = ""
        while inpt.lower() not in ("y", "n"):
            inpt = input("Are you sure you want to stop the server?(y/n) ").lower()

        return inpt == "y"

parser = argparse.ArgumentParser(description="Make an instance of the Electric Ballot",prog="EAVS")
parser.add_argument("candidates", nargs="?", help="a JSON file that holds the candidate list for the election")
parser.add_argument("config", default="default.json", nargs='?', help="a JSON file used as config for the program. See Documentation for details(default:default.json)")
args = parser.parse_args()

config = getConfig(args.config)
candidates = getCandidates(args.candidates, config["offices"])
offices = config["offices"]
officeCandidatesMaster = getOfficeCandidates(candidates)
dbConfig = config["db_config"]
serverConfig = config["server_config"]
pre_election = config["pre_election"]

masterCandidateList = parseMasterList(offices, officeCandidatesMaster)
AVSexception_handler = AVSDB.AVSExceptionHandler({AVSDB.AVSDBErrors.HasAlreadyRegisteredError: AVSDB.AVSExceptionHandler.POLICY_ASK})
mainAVS = AVSDB.AVSLogic(dbConfig["votes_db"], dbConfig["voter_db"], offices, masterCandidateList, AVSexception_handler, masterDBFile=dbConfig["master_db"], pre_election=pre_election)
serverAVS = AVS_Server.ClientAVSBridge(mainAVS, serverConfig["maxPCNum"], serverConfig["serverFolder"], JsonBackend())
serverTUI = AVSServerTUI(serverAVS)
print()
serverTUI.startElection()

