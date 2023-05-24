#!/usr/bin/python3
#TODO: Make an intermediate db class bc vote(r|s)DB share initialize() and checkField()
#add name/section/grade/party checking to Voter and Candidate classes
#DONE    so they won't be just dumb classes or just delegate that to input check?
#CAN'tDO: db must be closed for other pc's use;make con persistent through the db's lofe for efficiency and speed
#input sanitizer function, which filters non printable characters, whitespace, and names not in a database(optionally)
#exception handler when candidate is entered twice
#Move Non DB classes to separater class
#handle hashing/passwording
#DONEmake newVoterBallot respect voter's grade level
#DONEexclude office when there are no candidates
#Cover sqlite3.OperationalError bases (db locked, insufficient permissions, etc)

import sqlite3
import datetime
from pathlib import PurePath

import Core.AVSPrimitives as AVSPrimitives
import Core.AVSDBErrors as AVSDBErrors    #this or import all?

FileNotFoundError = IOError


class VoterDB(object):
    def __init__(self, dbFile):     #Handle: What if the voterDB suddenly became invalid?
        self.dbFile = str(PurePath(dbFile))
        if not self.isValidDB():
            print("VoterDB: The Database supplied ({}) is invalid. Initializing DB.".format(self.dbFile))
            self.clear()
        else:
            print("VoterDB: Database ({}) is valid.".format(self.dbFile))

    def clear(self):
        open(self.dbFile, "w").close()
        con = sqlite3.connect(self.dbFile)
        con.execute("CREATE TABLE Voters (StudentName VARCHAR(255), GradeLevel VARCHAR(2), Section VARCHAR(20), InTime VARCHAR(20), OutTime VARCHAR(20))")
        con.commit()
        con.close()

    def isValidDB(self):     #Refactor: remove clearing logic, just check integrity
        con = sqlite3.connect(self.dbFile)
        cur = con.cursor()

        try:
            cur.execute("SELECT StudentName, GradeLevel, Section, Intime, OutTime FROM Voters")
        except sqlite3.Error:
            return False
        finally:
            con.close()

        return True

    def checkField(self, field, voter):
        con = sqlite3.connect(self.dbFile)
        cur = con.cursor()
        arguments = (voter.name, voter.grade, voter.section)
        ####Sanitize field before query
        cur.execute("SELECT " + field + " FROM Voters WHERE StudentName = ? AND GradeLevel = ? AND Section = ?", arguments)
        row = cur.fetchone()
        con.close()

        return row

    def registerVoter(self, voter):
        con = sqlite3.connect(self.dbFile)

        inTime = self.checkField("InTime", voter)    #move to separate method later
        outTime = self.checkField("OutTime", voter)  # as it might be useful outside of registering voter
        if outTime not in (None, (None,)):
            #print(voter.name)
            #print("In time:", inTime)
            #print("Voter has already voted. Report to the technical team for false positives\n")
            raise AVSDBErrors.HasAlreadyVotedError
            #return False
        elif inTime not in (None, (None,)):
            #print(voter.name)
            #print("Voter already registered in database. Consult the technical team for help.\n")
            #return True    #more robustness later
            raise AVSDBErrors.HasAlreadyRegisteredError         #update inTime or nah?

        dateAndTime = datetime.datetime.now()
        dateAndTime = str(dateAndTime.date()) + " " + str(dateAndTime.time())
        arguments = (voter.name, voter.grade, voter.section, dateAndTime, None)
        con.execute("INSERT INTO Voters (StudentName, GradeLevel, Section, InTime, OutTime) VALUES (?, ?, ?, ?, ?)", arguments)
        con.commit()
        con.close()

        return True

    def registerOutTime(self, voter):
        con = sqlite3.connect(self.dbFile)

        inTime = self.checkField("InTime", voter)
        outTime = self.checkField("OutTime", voter)
        if inTime in (None, (None,)):
            print("VoterDB: Voter ({}) hasn't registered yet".format(voter))
            raise AVSDBErrors.VoterNotRegisteredError
        elif outTime not in (None, (None,)):
            print("VoterDB: An OutTime for the voter ({}) was already registered on the database. Consult the technical team".format(voter))
            raise AVSDBErrors.HasAlreadyVotedError

        dateAndTime = datetime.datetime.now()
        dateAndTime = str(dateAndTime.date()) + " " + str(dateAndTime.time())
        arguments = (dateAndTime, voter.name, voter.grade, voter.section)
        print("VoterDB: Recording the following data to the DB:", arguments, dateAndTime)
        con.execute("UPDATE Voters SET OutTime = ? WHERE StudentName = ? AND GradeLevel = ? AND Section = ?", arguments)
        con.commit()
        con.close()

class VotesDB(object):
    def __init__(self, dbFile, masterList=None, clear=False):
        self.dbFile = str(PurePath(dbFile))
        if self.isValidDB():
            print("VotesDB: Database ({}) is valid.".format(self.dbFile))    #dis or under try block?
        else:
            print("VotesDB: The Database supplied ({}) is invalid. Initializing DB.".format(self.dbFile))
            clear = True
            self.clear()

        if clear:
            self.initialize(masterList)

    def clear(self):
        open(self.dbFile, "w").close()
        con = sqlite3.connect(self.dbFile)
        con.execute("CREATE TABLE Candidates (CandidateName VARCHAR(255), Office VARCHAR(25), Party VARCHAR(255), Votes INT)")
        con.commit()
        con.close()

    def checkField(self, field, candidate):
        con = sqlite3.connect(self.dbFile)
        cur = con.cursor()
        arguments = (candidate.name, candidate.office, candidate.party)
        ####Sanitize field before query
        cur.execute("SELECT " + field + " FROM Candidates WHERE CandidateName = ? AND Office = ? AND Party = ?", arguments)
        row = cur.fetchone()
        con.close()

        return row

    def isValidDB(self):    #refactor to isValid boolean function then move clearing logic to initialize
        con = sqlite3.connect(self.dbFile)
        cur = con.cursor()

        try:
            cur.execute("SELECT CandidateName, Office, Party, Votes FROM Candidates")
        except sqlite3.Error:       #Generic catch; was just OperationalError before
            return False
        finally:
            con.close()

        return True

    def initialize(self, masterList):       #Remove prints here
        con = sqlite3.connect(self.dbFile)
        cur = con.cursor()

        print("VotesDB: Initializing DB ({}) with the following Candidates:".format(self.dbFile))
        for officeName in masterList.keys():
            office = masterList[officeName]
            for candidate in office:
                candidateDataInDB = self.checkField("*", candidate)
                if candidateDataInDB not in (None, (None,)):
                    print("VotesDB: Candidate ({}) already in the database. Skipping".format(candidate))
                    continue

                print(" ", candidate)
                args = (candidate.name, candidate.office, candidate.party, 0)
                cur.execute("INSERT INTO Candidates (CandidateName, Office, Party, Votes) VALUES (?, ?, ?, ?)", args)

        print()
        con.commit()
        con.close()

    def incrementVote(self, candidateList):     #handle [permission, non-existen candidate] errors here
        con = sqlite3.connect(self.dbFile)
        cur = con.cursor()
        for candidate in candidateList:
            args = [candidate.name, candidate.office, candidate.party]
            args.extend(args)        #*2 because of the inner args required by getting the current number of votes
            cur.execute("UPDATE Candidates SET Votes = (SELECT Votes FROM Candidates WHERE CandidateName = ? aND Office = ? AND Party = ?) + 1 WHERE CandidateName = ? AND Office = ? AND Party = ?", args)

        con.commit()
        con.close()

class MasterDB(object):     #Hacky for now, like all things;    continue dat avsdb baseclass and add createTable method (which updates the db with a new AVSTable instance)
    #Manages a Table of the master list of valid voters with the following format(subject to change):
    #<Table> Grade Level 1
    #   <cells> Name Section
    #<Table> Grade Level 2
    #   <cells> Name Section
    #etc.
    def __init__(self, dbFile, masterList=None):
        self.dbFile = str(PurePath(dbFile))

        try:
            open(self.dbFile, "r")
        except (FileNotFoundError, IOError):
            self.dbFile = None

        if self.dbFile is None:
            print("No db file supplied; assuming masterDB is not needed")
            return
        elif masterList is None:
            print("MasterDB: Database ({}) should be already Valid.".format(self.dbFile))     #ungraceful and not robust; should be just placeholder
            return      #maybe check db for validity?
        elif isinstance(masterList, str):
            masterList = json.load(open(PurePath(masterList), "r"))     ####Check if file exists first
        elif isinstance(masterList, dict):
            pass
        else:
            return      #raise TypeError?

        self.initialize(masterList)
        print("MasterDB: Initialized Database", dbFile)

    def initialize(self, masterList):
        #MasterList here should be a json file (subject to change) with the following format:
        #{"Grade Level 1": {
        #       "Section1": <Here goes the names, Sur, First, MI>
        #       "Section2": <Here goes the names, Sur, First, MI>
        #   },
        #"Grade Level 2": { etc
        #open(self.dbFile, "w").close() #for debug only
        con = sqlite3.connect(self.dbFile)
        cur = con.cursor()
        for gradeLevel in masterList.keys():     #Use sanitize input from dat avsdb base rework first?
            cur.execute("CREATE TABLE 'Grade {}' (StudentName VARCHAR(255), Section VARCHAR(20))".format(gradeLevel)) #handle if table already exists
            for section in masterList[gradeLevel].keys():
                for student in masterList[gradeLevel][section]:
                    args = (student, section)
                    cur.execute("INSERT INTO 'Grade {}' (StudentName, Section) VALUES (?, ?)".format(gradeLevel, args))
        con.commit()
        con.close()

    def checkVoter(self, name, grade, section):    #needs more concise name, + take in voter or separate name, grade, section?
        #name = voter.name
        #grade = voter.grade
        #section = voter.section

        if self.dbFile is None:
            return True

        con = sqlite3.connect(self.dbFile)   #No need to create cur?
        try:
            args = (name, section)
            rows = con.execute("SELECT * FROM " + ('"Grade ' + str(grade + '"')) + "WHERE StudentName = ? AND Section = ?", args).fetchone()
        except sqlite3.Error:
            print("MasterDB: Invalid grade Level Supplied", grade)    #debug for now
            #raise InvalidGradelevelError?
        else:
            if rows in (None, (None, )):
                return False
            else:
                return True

################################These are only used by AVSComboBoxText for now
    def getStudentInfo(self, name):
        if self.dbFile is None:
            return  (None, None)

        con = sqlite3.connect(self.dbFile)
        cur = con.cursor()
        gradeLevels = cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
        gradeLevels = [grade[0] for grade in gradeLevels]

        for grade in gradeLevels:       #does not handle duplicate names for now
            section = cur.execute("SELECT Section FROM '{}' WHERE StudentName = ?".format(grade), (name, )).fetchone()
            if section not in (None, (None, )):
                return (grade.lstrip("Grade "), section[0])

        return (None, None)

    def getAllNames(self):      #hacky and dirty
        if self.dbFile is None:
            return []

        con = sqlite3.connect(self.dbFile)
        cur = con.cursor()
        gradeLevels = cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
        gradeLevels = [grade[0] for grade in gradeLevels]

        names = []
        for grade in gradeLevels:
            sections_raw = cur.execute("SELECT Section FROM  '{}' ".format(grade)).fetchall()
            sections = []
            for section in sections_raw:
                if section[0] not in sections:
                    sections.append(section[0])

            for section in sections:
                names_local = cur.execute("SELECT StudentName FROM '{}' WHERE Section = ?".format(grade), (section, )).fetchall()
                names_local = [name[0] for name in names_local]
                #print(section, names_local)
                names.extend(names_local)

        return names

    def getAllGrades(self):
        if self.dbFile is None:
            return []

        con = sqlite3.connect(self.dbFile)
        cur = con.cursor()
        gradeLevels = cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
        gradeLevels = [grade[0].lstrip("Grade ") for grade in gradeLevels]

        return gradeLevels

    def getAllSections(self):
        if self.dbFile is None:
            return []

        con = sqlite3.connect(self.dbFile)
        cur = con.cursor()
        gradeLevels = cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
        gradeLevels = [grade[0] for grade in gradeLevels]

        sections = []
        for grade in gradeLevels:
            sections_raw = cur.execute("SELECT Section FROM  '{}' ".format(grade)).fetchall()
            for section in sections_raw:
                if section[0] not in sections:
                    sections.append(section[0])

        return sections

    def __addVoter(self):       #Password protected; should be for edge cases only
        pass

class AVSExceptionHandler(object):
    #Move these to an enum
    POLICY_WARN = "==WARN=="        #may be uneeded/ there is no apparent way to make this work
    POLICY_BLOCK = "==BLOCK=="
    POLICY_IGNORE = "==IGNORE=="
    POLICY_ASK = "==ASK=="

    def __init__(self, policies=None, default_policy=POLICY_BLOCK):
        print("AVSExceptionHandler: Default Policy:", default_policy)
        if policies is None:
            policies = {}

        self.exception_stack = []
        self.default_policy = default_policy
        self.policies = policies

        ####For UI hook functions
        self.on_append_callbacks = []
        self.on_block_callbacks = []
        self.on_allow_callbacks = []

    def query_policy(self, exception):
        if exception in self.policies.keys():
            return self.policies[exception]
        else:
            return self.default_policy

    def add_to_queue(self, exception, voter, data=None):
        data = {"Voter": voter, "Exception": type(exception), "Data": data}     #type(exception) or just exception?; make a dedicated aehError class?

        self.exception_stack.append(data)
        for callback in self.on_append_callbacks:
            callback(exception)

    def allow_exception(self, exception, voter):        #TODO: Maybe create an AVSExceptionHandled object instead of returning either the data or False
        for item in self.exception_stack[::-1]:
            if item["Voter"] == voter and item["Exception"] == type(exception):
                for callback in self.on_allow_callbacks:
                    callback(exception)
                self.exception_stack.remove(item)

                return item["Data"]

        print("AVSExceptionHandler: Debug: Error! Exception not found in the stack(allow_main)")
        return False

    def block_exception(self, exception, voter):        #almost 1:1 copy of .allow_exception()
        for item in self.exception_stack[::-1]:
            if item["Voter"] == voter and item["Exception"] == type(exception):
                for callback in self.on_block_callbacks:
                    callback(exception)
                self.exception_stack.remove(item)

                return False

        print("AVSExceptionHandler: Debug: Error! Exception not found in the stack(block)")
        return False

    def register_callback(self, callback, signal="append"):
        if callback is None:
            return

        if signal == "append":
            self.on_append_callbacks.append(callback)
        elif signal == "allow":
            self.on_allow_callbacks.append(callback)
        elif signal == "block":
            self.on_block_callbacks.append(callback)

class AVSLogic(object):
    def __init__(self, votesDBFile, voterDBFile, offices, masterCandidateList, AVSexception_handler, masterDBFile=None, reset=False, pre_election=True):
        self.masterCandidateList = masterCandidateList
        self.AVSexception_handler = AVSexception_handler
        self.votesDB = VotesDB(votesDBFile, masterCandidateList)
        self.voterDB = VoterDB(voterDBFile)
        self.masterDB = MasterDB(masterDBFile)
        self.offices = offices
        self.grade_offset = int(pre_election)    #If it is a pre election, then officers for the next school year are to be voted for, and Grade Representatives have to be one grade higher

        if reset:
            self.clear(masterCandidateList)

    def startElection(self):
        pass        #overload in other cases to make custom setup

    def stopElection(self):
        pass    #overload in other cases to customize the election end

    def clear(self, masterCandidateList):      #ayusin
            self.votesDB.clear()
            self.votersDB.clear()
            self.votesDB(masterCandidateList)      #wat

    def newVoterBallot(self, name, grade, section):
        voter = AVSPrimitives.Voter(name, grade, section)
        if not self.masterDB.checkVoter(name, grade, section):
            self.handleError(AVSDBErrors.VoterNotInDatabaseError, voter, voter)

        #TODO: Process offices first (Handle Grade %grade Representative); maybe create a decicated offices class?
        offices = []        #Condense into one line using filter? + any?
        for office in self.offices:     #hardcoded for now
            if office.startswith("Grade"):
                if str(int(grade) + self.grade_offset) in office:
                    offices.append(office)
            else:
                offices.append(office)

        ballot = AVSPrimitives.Ballot(voter, offices, self.masterCandidateList)
        try:
            self.voterDB.registerVoter(voter)
        except AVSDBErrors.AVSDBError as error:
            self.handleError(error, voter, ballot)

        return ballot

    def processBallot(self, ballot):
        if ballot is None:
            print("AVSLogic: Invalid ballot. Either voter has already voted, or ballot was Corrupted.")
            return      #raise AVSDB.InvalidBallot

        voter = ballot.voter
        offices = ballot.offices
        if voter is None:
            print("AVSLogic: Invalid Ballot (No voter)")
            return      #raise NoVoterInfoError

        votedCandidates = []
        for office in offices:
            officeClass = None
            try:
                officeClass = getattr(ballot, office)
            except AttributeError:
                print("AVSLogic: ", office, "not in ballot")      #raise
                continue

            voted = officeClass.votedCandidate
            if voted is None:
                continue
            elif not self.masterDB.checkVoter(voter.name, voter.grade, voter.section):
                print("AVSLogic: Oops! A voter not in the database is trying to submit ballot! This should be unreachable")
                self.handleError(AVSDBErrors.VoterNotInDatabaseError, voter, voter)
            else:
                votedCandidates.append(voted)

        try:
            self.voterDB.registerOutTime(voter)
        except AVSDBErrors.AVSDBError as error:
            self.handleError(error, voter, ballot)
        else:
            self.votesDB.incrementVote(votedCandidates)

    def handleError(self, error, voter, data=None):
        policy =  self.AVSexception_handler.query_policy(type(error))
        error.policy = policy
        error.voter = voter
        if policy == self.AVSexception_handler.POLICY_BLOCK:
            raise error
        elif policy == self.AVSexception_handler.POLICY_IGNORE:
            return
        elif policy == self.AVSexception_handler.POLICY_ASK:
            self.AVSexception_handler.add_to_queue(error, voter, data)
            error.ballot = data     #stop gap for now; migrate soon
            raise error
        else:
            raise error

    def ask_error_handling(self, error, voter, ui_callback=None):       ####Unused for now
        #handle if error is in stack first?
        if ui_callback is None:
            ui_callback = self.mainServerQueryTUI
            print("NON: ui_callback not specified")
            #return False

        data = None
        if ui_callback(error, voter):
            data = self.AVSexception_handler.allow_exception(error, voter)
        else:
            self.AVSexception_handler.block_exception(error, voter)
        return data

    ####These should be defined by a UI implementation; Defined here bc there is no clean way to make it accessible to stand-alone mode, too
    def mainServerQuery(self, error, voter):    #This should be in the main server gui, outside?
        import gi       #HAx on top oh HaX
        gi.require_version("Gtk", "3.0")
        from gi.repository import Gtk

        #maybe do this in a separate thread, then get response through a promise/future so that ui is not locked during querying
        message = "Voter {} is asking permission to re-entry for thr Error: {}".format(voter, error.message)
        dialog = Gtk.MessageDialog(None, None, Gtk.MessageType.QUESTION, (Gtk.STOCK_NO, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK), error.message)
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.OK:
           return  True
        else:
            return False

    def mainServerQueryTUI(self, error, voter):
        allow = input("mainAVS: Should voter {} be allowed to vote?\nHe/she has committed the following sin: {} (y/N ): ".format(voter, error.message)).lower()
        return allow == "y"


if __name__ == "__main__":
    from Core.AVS_Misc_Utilities import parseMasterList
    masterList = {
        "Sum Party": {
            "President": "Wyan Waminal",
            "Vice President": "Sumwam else",
            "Treasurer": "Austin Dewa Kwuz"
            },

        "Real Party": {
            "President": "Ryan Jaminal",
            "Vice President": "Vincent Dela Cruz",
            "Treasurer": "Austin Dela Cruz"
            },

        "Fake Party": {
            "President": "Ryan Jaminal (Fake)",
            "Treasurer": "Aso"
            }
        }

    AVSexception_handler = AVSExceptionHandler()
    offices = ["President", "Vice President", "Treasurer"]
    masterCandidateList = parseMasterList(offices, masterList)
    print("master list:", masterCandidateList)
    mainAVS = AVSLogic("votesDB.db", "voterDB.db", offices, masterCandidateList,  AVSexception_handler)

    def voteSequence(ballot):
        if ballot is None:
            return

        offices = ballot.offices
        for office in offices:
            officeClass = getattr(ballot, office)
            candidates = officeClass.candidateList
            print(office, ":")
            for index, candidate in enumerate(candidates):
                print(index + 1, candidate.name, " from ", candidate.party)

            inpt = ""
            while not inpt.isnumeric():
                inpt = str(input("Choose the index of your  candidate (0 for none)"))

            inpt = int(inpt)
            if inpt == 0:
                candidate = None
            else:
                candidate = candidates[inpt - 1]

                ballot.vote(candidate.office, candidate)

        mainAVS.processBallot(ballot)

    ballot = mainAVS.newVoterBallot("Jami", "11", "MCL")
    if ballot != None:
        print(ballot.President)
        ballot._spillBallot(offices)
        #ballot.vote(masterCandidateList["President"][0])
        #ballot._spillBallot(offices)
        #ballot.vote(masterCandidateList["President"][1])
        #ballot._spillBallot(offices)
        #ballot.vote(masterCandidateList["Vice President"][0])
        ballot.vote(AVSPrimitives.Candidate("President", "Ryan Jaminal", "President",  "Real Party"))
        ballot._spillBallot(offices)
        ballot.vote(AVSPrimitives.Candidate("President", "Sumwam erusu", "President", "LALa land"))
        ballot._spillBallot(offices)
        mainAVS.processBallot(ballot)
        ballot = mainAVS.newVoterBallot("lul", "11", "MCL")
        ballot._spillBallot(offices)
        mainAVS.processBallot(ballot)

    ballot = mainAVS.newVoterBallot("jp", "10", "Einstein")
    ballot = AVSPrimitives.Ballot(AVSPrimitives.Voter("lel", "11", "rizael"), mainAVS.offices, mainAVS.masterCandidateList)
    voteSequence(ballot)
    name = ""
    while name != "STAHP":
        name = str(input("Name: "))
        ballot = mainAVS.newVoterBallot(name, 10, "Einstein")
        voteSequence(ballot)

    print("\n\n")
    print("----------------------------------------")

"""
    candidates = []
    candidate = Candidate("jaminal", "President", "Turks Party")
    candidates.append(candidate)

    name =""
    while name != "STAHP":
        name = str(input("Candidate Name:"))
        office = str(input("Office: "))
        candidate = Candidate(name, office, "Turks Party")
        candidates.append(candidate)

    votesDB = VotesDB("/mnt/sdcard/votesDB_trial.db", candidates)
    votesDB.incrementVote(candidates)
    for i in ("7 times"):
        votesDB.incrementVote(candidates[:3])
"""
