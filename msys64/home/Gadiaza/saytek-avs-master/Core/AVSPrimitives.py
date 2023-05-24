#!/usr/bin/env python3

class Voter(object):
    def __init__(self, name, grade, section):
       self.name = name
       self.grade = grade
       self.section = section

    def __eq__(self, voter):
        if voter == None:
            return False

        return ((self.name == voter.name)
            and (self.grade == voter.grade)
            and (self.section == voter.section))

    def __str__(self):
        return(self.name + " from Grade " + self.grade + " " + self.section)

class Candidate(object):
    def __init__(self, name, office, party):
        self.name = name
        self.office = office
        self.party = party

    def __str__(self):
        return self.name + " from " + self.party

    def __eq__(self, candidate):
        if not isinstance(candidate, Candidate):
            return False
        return ((self.name == candidate.name)
            and (self.office == candidate.office)
            and (self.party == candidate.party))

class Office(object):
    def __init__(self, officeName, candidates):
        self.officeName = officeName
        self.candidateList = candidates
        self.votedCandidate = None

    def __contains__(self, candidate):
        for c in self.candidateList:
            if (c == candidate):
                return True

        return False

    def voteCandidate(self, candidate):
        if candidate == None:
            self.votedCandidate = None
        elif candidate in self:
            self.votedCandidate = candidate
        #else:
            #raise CandidateNotInOfficeError

class Ballot(object):               #IMPROV: Make only fields voted on actually exist on the object to save space?
    def __init__(self, voter, offices, masterList):
        self.voter = voter
        self.offices = offices
        for office in self.offices:
            try:
                officeClass = Office(office, masterList[office])
            except KeyError:
                print(office, "not in offices") #raise
            else:
                setattr(self, office, officeClass)

    def vote(self, office, candidate):
        officeClass = getattr(self, office)
        officeClass.voteCandidate(candidate)

    def _spillBallot(self, offices):
        try:
            print("Voter Info:")
            print("Name:", self.voter.name)
            print("Grade:", self.voter.grade)
            print("Section:", self.voter.section)
        except AttributeError:
            print("None")

        for office in offices:
            officeClass = getattr(self, office)
            voted = None
            try:
                voted = officeClass.votedCandidate
            except AttributeError:
                pass

            print(office + ":",  voted,)
        print()
