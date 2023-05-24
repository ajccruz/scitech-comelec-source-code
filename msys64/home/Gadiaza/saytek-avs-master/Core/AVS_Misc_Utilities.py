#!/usr/bin/env python3

import json     #for getConfig
import time    #Used by waitForFile() and waitForFileDeletion()
import os

from pathlib import PurePath


import Core.AVSPrimitives as AVSPrimitives    #Used by parseMasterList
import Core.AVSDBErrors as AVSDBErrors
####File I/O#######################################################################################
def waitForFile(fileName, mode="r", delay=0.2, blocking=True, **kwargs):    #why?
    fileName = str(PurePath(fileName))
    while True:
        #os.access() used as it is faster than a try block, plus it also takes into account permissions
        if not os.access(fileName, os.F_OK):
            if not blocking:
                time.sleep(delay)       #delay still used here so that when caller for some reason calls this for a long enough time, it still won't hog resources, e.g. When the blocking behaviour is actually needed, but the caller wanted to print a debug message for each call so blocking was set to false, but the call is still enclosed in a while True loop
                raise FileNotFoundError()

            time.sleep(delay)
            continue

        #The below try block is a safety net for times when the file is deleted in the small gap of time between the call to os.access and open(), in which the program would crash without this try block
        try:
            ###Only allow these as modes?: "w", "a", "bw", "aw"
            fil = open(fileName, mode, **kwargs)
        except FileNotFoundError:
            if not blocking:
                time.sleep(delay)       #delay still used here so that when caller for some reason calls this for a long enough time, it still won't hog resources, e.g. When the blocking behaviour is actually needed, but the caller wanted to print a debug message for each call so blocking was set to false, but the call is still enclosed in a while True loop
                raise

            time.sleep(delay)
            continue
        else:
            return fil

def waitForFileDeletion(fileName, mode="r", delay=0.2, blocking=True, **kwargs):
    fileName = str(PurePath(fileName))
    while True:
        #No need to use a try-open-catch here as race conditions won't matter, We're only checking for a file's existence
        if not os.access(fileName, os.F_OK):
            return True
        else:
            if not blocking:
                time.sleep(delay)       #delay still used here so that when caller for some reason calls this for a long enough time, it still won't hog resources
                return False

            time.sleep(delay)
            continue
##################################################################################################

####Config Translation helper functions############################################################
def getNonPartyKeys(configFile):
    return ["ui_config", "offices"]

def getPartyKeys(configFile):
    nonPartyKeys = getNonPartyKeys(configFile)
    return [key for key in configFile.keys() if key not in nonPartyKeys]

def getOfficeCandidates(configFile):
    parties = getPartyKeys(configFile)

    officeCandidatesMaster = {}
    for party in parties:
        officeCandidatesMaster[party] = configFile[party]

    return officeCandidatesMaster
""""
    officeCandidatesMaster = {}
    for office in configFile[offices"offices"]:
        officeCandidatesMaster[office] = []

    for party in parties:
        print(party)
        currentParty = configFile[party]
        print(currentParty)
        for office in currentParty.keys():
            officeCandidatesMaster[office].append(currentParty[office])
"""
def parseMasterList(offices, masterList):
    masterCandidateList = {}
    for office in offices:
        masterCandidateList[office] = []
    for partyName in sorted(list(masterList.keys())):       #sorted() here makes the order of parties alphabetically sorted
        party = masterList[partyName]
        if partyName.lower() == "independent":      #The party key "Independent" (case insensitive) is reserved for independent candidates and takes the form of a list with offices as keys and has a value of a list of independent candidates
            for office in party:
                masterCandidateList[office].extend(map(lambda candidate: AVSPrimitives.Candidate(candidate, office, partyName), party[office]))
            continue

        print("parseMasterList: parsing party", partyName)
        for office in party.keys():
            candidate = party[office]
            candidateClass  = AVSPrimitives.Candidate(candidate, office, partyName)
            masterCandidateList[office].append(candidateClass)

    return masterCandidateList

def getConfig(configFile):
    configFile = str(PurePath(configFile))
    try:
        configFile = open(configFile, "r")
    except IOError:
        print("#######################################################################################")
        print("#Error: The file (%s) can't be found or read." % configFile)
        print("#Make sure that the file exists and that you have at least read permissions to it.")
        print("#Falling back to the default config.json")
        print("#######################################################################################\n")
        configFile = open("default.json", "r")

    if configFile == "default.json":
        print("Default config loaded")

    print("Loading config ({})".format(configFile.name))
    try:
        config = json.load(configFile)
        required_keys = {
        "ui_config": [
            "assetsFolder",
            "pictureFormat",
            "officeBoxSpacing",
            "maxOfficesPerColumn",
            ],

        "db_config": [
            "votes_db",
            "voter_db",
            "master_db"
            ],

        "server_config": [
            "serverFolder",
            "maxPCNum"
            ],

        "offices" : []
        }
        for key in required_keys:
            for subkey in required_keys[key]:
                try:
                    config[key][subkey]     #Try accessing the config option to see if it exists
                except KeyError:
                    raise AVSDBErrors.AVSConfigError("The key and subkey '" + key + " " + subkey + "' are required but are not found in the config supplied.")
    except (FileNotFoundError, IOError, KeyError):
        raise AVSDBErrors.AVSConfigError(AVSDBErrors.AVSConfigError.message)

    return config

def getCandidates(candidatesFile, offices):
    candidatesFile = str(PurePath(candidatesFile))
    try:
        candidatesFile = open(candidatesFile, "r")
    except IOError:
        print("#######################################################################################")
        print("#Error: The file (%s) can't be found or read." % candidatesFile)
        print("#Make sure that the file exists and that you have at least read permissions to it.")
        print("#Falling back to the default candidates.json")
        print("#######################################################################################\n")
        candidatesFile = open("default.json", "r")

    if candidatesFile == "default.json":
        print("Default candidates loaded")

    print("Loading candidates ({})".format(candidatesFile.name))
    try:
        candidates = json.load(candidatesFile)
        for key in candidates:
            for office in candidates[key]:
                if office not in offices:
                    raise KeyError("Office in the config is not in the valid offices.")     #Shouldn't be a KeyError, but will have to do for now

    except (FileNotFoundError, IOError, KeyError):
        raise AVSDBErrors.AVSCandidatesFileError(AVSDBErrors.AVSCandidatesFileError.message)

    return candidates


##################################################################################################

def centerText(*args):
    max_len = max(len(arg) for arg in args)

    output = []
    for arg in args:
        output.append(arg.center(max_len))

    return tuple(output)


