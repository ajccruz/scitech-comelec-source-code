#!/usr/bin/env python3

"""
Defines functions related to rearranging the DB used by the ui completion.
This is done so that only the relevant students are auto-completed and also
prevent data leakage as knowing a student's name enables an exploiter to gain
information of the student through the ui completion.
"""

import sqlite3

import AVSDB       #For MasterDB


def repopulate_completionDB(completionDB_filename, masterCompletionDB_filename, grade_levels=None, sections=None):       #Maybe make it take a new masterList (non-db), though that might be more susceptible to bait and switch attacks
    """
    creates a MasterDB from the avaible info in the supplied masterCompletionDB,
    with optional grade and section limiters.
    """
    
    masterCompletionDB = AVSDB.MasterDB(masterCompletionDB_filename)
    if grade_levels == None:
        grade_levels = masterCompletionDB.getAllGrades()
    if sections == None:
        sections = masterCompletionDB.getAllSections()

    grades = [grade for grade in grade_levels if str(grade) in masterCompletionDB.getAllGrades()]
    allowed_sections = [section for section in sections if str(section) in masterCompletionDB.getAllSections()]

    new_masterList = {}
    con = sqlite3.connect(masterCompletionDB.dbFile)
    cur = con.cursor()
    for grade in grades:
        new_masterList[grade] = {}
        for section in allowed_sections:
            names = cur.execute("SELECT StudentName FROM 'Grade %s' WHERE Section='%s'" % (grade, section)).fetchall()
            names = [name[0] for name in names]    
            new_masterList[grade][section] = names

    AVSDB.MasterDB(completionDB_filename, new_masterList)

if __name__ == "__main__":
    new_DB_name = "test_completionDB.db"
    repopulate_completionDB(new_DB_name, "masterDB_tui.db", [10, 9], ["Einstein", "Dalton"])
