#!/usr/bin/env python3

#TODO: separate DB Errors from main Logic errors (might include mirroring/building upon existing DB Errors
#Remove unused errors or actually make use of them?

#This base Exception shouldn't be in a file named AVSDBErrors, but maybe the filename is what should be changed.
class AVSError(Exception):
    message = "An AVS-related error has occured."
    policy = None

class AVSBackendError(AVSError):
    message = "An error has occured in the backend."
    policy = None

class InvalidEncodeRequestError(AVSBackendError):
    message = "The data supplied to the backend's encoder can not be serialized. Check for the data's integrity and if not already supported, add functionality to the backend if encoding this type of data is desired."

class InvalidDecodeRequestError(AVSBackendError):
    message = "Data requested for decoding is either corrupted or Invalid. Check if decoding it is suppported by the backend or check it's integrity."

class AVSConfigError(AVSError):
    message = "An Invalid or corrupted AVS config was supplied."

class AVSCandidatesFileError(AVSError):
    message = "The candidates file supplied is either invalid or corrupted."

class AVSServerConnectionError(AVSError):
    message = "Communication with the AVS Server failed. Check if the AVS Server is initialized and proper setup is done for communication with Clients."

class AVSServerUninitializedError(AVSError):
    message = "The AVS Server was not initialized properly. Check the setup for any mistakes or deficiencies."

class AVSDBError(AVSError):
    message = "A Non-identifiable Error involving an AVS Database occured."
    policy = None
    voter = None

class InvalidAVSDatabaseError(AVSDBError):
    message = "The AVS Database supplied is invalid."

class VoterNotInDatabaseError(AVSDBError):
    message = "Voter is not in the Database of valid voters."

class HasAlreadyVotedError(AVSDBError):
    message = "Voter has Already voted."

class HasAlreadyRegisteredError(AVSDBError):
    message = "Voter has Already registered."

class VoterNotRegisteredError(AVSDBError):
    message = "Voter hasn't registered yet."

class BallotError(AVSDBError):
    message = "A Non-identifiable Error involving voter Ballots has occured."

class NoVoterInfo(BallotError):
    message = "The Ballot Supplied does not have voter information."

