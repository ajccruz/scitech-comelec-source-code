#!/usr/bin/env python3

import json     #For the json backend
#import pickle   #For the pickle backend

import Core.AVSPrimitives as AVSPrimitives
import Core.AVSDBErrors as AVSDBErrors


class JsonBackend(object):        #make stuff staticmethods?; encode, decode -> loads, dumps?
    def encode(self, data, extra_data=None):
        if isinstance(data, AVSPrimitives.Voter):
            return self.encodeVoter(data, extra_data)
        elif isinstance(data, AVSPrimitives.Candidate):
            return self.encodeCandidate(data, extra_data)
        elif isinstance(data, AVSPrimitives.Ballot):
            return self.encodeBallot(data, extra_data)
        elif isinstance(data, AVSDBErrors.AVSDBError):
            return self.encodeError(data, extra_data)
        elif data in (None, {}):        #Should this be spceial cased or a generic return on unrecognized types be used instead of raising?
            return {}
        else:
            raise AVSDBErrors.InvalidEncodeRequestError

    def encodeVoter(self, voter, extra_data=None):
        if extra_data is None:
            extra_data = {}

        voter_encoded = {"Name": voter.name, "Grade": voter.grade, "Section": voter.section}
        voter_encoded.update(extra_data)

        return voter_encoded

    def encodeCandidate(self, candidate, extra_data=None):
        if extra_data is None:
            extra_data = {}

        candidate_encoded = {"Name": candidate.name, "Office": candidate.office, "Party": candidate.party}
        candidate_encoded.update(extra_data)

        return candidate_encoded

    def encodeBallot(self, ballot, extra_data=None):
        if extra_data is None:
            extra_data = {}

        ballot_encoded = {}
        for office in ballot.offices:
            ballot_encoded[office] = {"Candidates": []}
            officeClass = getattr(ballot, office)
            for candidate in officeClass.candidateList:
                ballot_encoded[office]["Candidates"].append(self.encodeCandidate(candidate))
            if officeClass.votedCandidate is not None:
                ballot_encoded[office]["Voted"] = self.encodeCandidate(officeClass.votedCandidate)

        ballot_encoded["Voter"] = self.encodeVoter(ballot.voter)
        ballot_encoded["Offices"] = ballot.offices      #.encode(offices)?
        ballot_encoded.update(extra_data)

        return ballot_encoded

    def encodeError(self, error, extra_data=None):
        if extra_data is None:
            extra_data = {}

        encoded_error = {}
        encoded_error["Error"] = str(type(error))
        encoded_error["Voter"] = self.encodeVoter(error.voter)
        encoded_error["Policy"] = error.policy
        encoded_error.update(extra_data)

        return encoded_error
 
    def decode(self, encoded_data):     #Very hacky, but managebale; a config restructuring might be needed
        keys = encoded_data.keys()
        if "Error" in keys:
            return self.decodeError(encoded_data)
        elif ("Office" in keys) and ("Party" in keys):
            return self.decodeCandidate(encoded_data)
        elif ("Grade" in keys) and ("Section") in keys:
            return self.decodeVoter(encoded_data)
        elif "Offices" in keys:
            return self.decodeBallot(encoded_data)
        elif len(keys) <= 1:        #very hardcoded; means that only clientID might be present
            return None
        else:
            raise AVSDBErrors.InvalidDecodeRequestError
     
    def decodeVoter(self, encoded_voter):
        name = encoded_voter["Name"]
        grade = encoded_voter["Grade"]
        section = encoded_voter["Section"]

        return AVSPrimitives.Voter(name, grade, section)

    def decodeCandidate(self, encoded_candidate):
        name = encoded_candidate["Name"]
        office = encoded_candidate["Office"]
        party = encoded_candidate["Party"]

        return AVSPrimitives.Candidate(name, office, party)

    def decodeBallot(self, ballot_encoded):
        masterList = {}
        for office in ballot_encoded["Offices"]:
            masterList[office] = []
            for candidate_encoded in ballot_encoded[office]["Candidates"]:
                masterList[office].append(self.decodeCandidate(candidate_encoded))

        voter = self.decodeVoter(ballot_encoded["Voter"])
        offices = ballot_encoded["Offices"]
        ballot = AVSPrimitives.Ballot(voter, offices, masterList)

        for office in offices:
            try:
                candidate = self.decodeCandidate(ballot_encoded[office]["Voted"])
            except KeyError:        #Catches both invalid office and no voted candidate
                continue
            else:
                ballot.vote(office, candidate)

        return ballot

    def decodeError(self, encoded_error):
        errors = (
            AVSDBErrors.VoterNotInDatabaseError,
            AVSDBErrors.HasAlreadyRegisteredError,
            AVSDBErrors.HasAlreadyVotedError,
            AVSDBErrors.VoterNotRegisteredError,
            AVSDBErrors.AVSDBError
        )

        encoded_error_type = encoded_error["Error"]
        #print("Error:", encoded_error_type)
        for error in errors:
            if str(error) in encoded_error_type:         #<in> is used because the same exception might be raised not direclty fro AVSDBErrors, therefore its str() representation changes
                error.policy = encoded_error["Policy"]
                error.voter = self.decodeVoter(encoded_error["Voter"])
                return error()        #return class or instance?

        raise Exception     #Should be unreachable, unless something corrupts the json
