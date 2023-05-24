#!/usr/bin/env python3
#TODO: add fallback photo for when photo is not supplied for candidate
#find a way to center the main voting screen
#Fix the office box class (refactor)
#   -add self.voted attribute to be changed; acts as "semaphore"
#   -do the same for all the things requiring a reference to mainAVS
#actually use the config options
#All things concerning modals are a product of cargo cult programming; fix, pls

from pathlib import PurePath

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import Core.AVSDB as AVSDB    #For Main avs logic
from Core.AVS_Misc_Utilities import centerText


####Here be Legacy stuff#
class LegacyOfficeBox(Gtk.Box):
    def __init__(self, officeClass, *args, **kwargs):
        Gtk.Box.__init__(self, *args, **kwargs)
        self.office = officeClass

        office_label = Gtk.Label(officeClass.officeName)
        self.AVSCBB = AVSLegacyComboBox(officeClass.candidateList)
        self.AVSCBB.set_size_request(1000, -1)      #Hardcoded combobox width for now so i wouldn't have to deal with aligning the combobox starts bc of varying officeName length
        clear_button = Gtk.Button.new_from_icon_name("edit-clear", Gtk.IconSize.BUTTON)

        self.AVSCBB.connect("changed", self.candidateChosen)
        clear_button.connect("clicked", self.clearVoted)

        hbox = Gtk.Box()
        self.pack_start(office_label, False, False, 0)
        hbox.pack_end(clear_button, False, False, 0)
        hbox.pack_end(self.AVSCBB, False, False, 0)

        clear_button.set_margin_start(30)   #Hardcoded

        self.pack_start(hbox, True, True, 0)

    def candidateChosen(self, AVSCBB):
        voted = AVSCBB.get_voted_candidate()
        self.office.voteCandidate(voted)

    def clearVoted(self, clearButton):      #Merger to candidateChosen?
        self.office.voteCandidate(None)
        self.AVSCBB.set_active(-1)        #Clears the combobox

class AVSLegacyComboBox(Gtk.ComboBoxText):
    def __init__(self, candidates, *args, **kwargs):
        Gtk.ComboBoxText.__init__(self, *args, **kwargs)
        self.candidates = [None]        #Made for cancelling vote/so that the first field points to nobody; improve soon
        self.candidates.extend(candidates)

        for candidate in self.candidates:
            if candidate is None:
                self.append_text("")
            else:
                self.append_text(candidate.name)

    def get_voted_candidate(self):
        voted_index = self.get_active()     #Relies on the fact that the order of self.candidates is the same order the candidate's name is appended to the combobox
        if voted_index == -1:        #Special cased as Selecting none in the combobox returns -1, which is still valid in python
            voted_index = None

        voted = None
        if voted_index is not None:
            voted = self.candidates[voted_index]

        return voted

class AVSLegacyMainVotingScreen(Gtk.Box):
    def __init__(self, config, *args, **kwargs):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.config = config

    def run(self, ballot, mainAVS, orderedStack):
        self.ballot = ballot    #Should the ballot even be owned? The only addition to accessible data is the voter's info
        mainBox = Gtk.FlowBox()
        mainBox.set_orientation(Gtk.Orientation.VERTICAL)
        mainBox.set_min_children_per_line(5)
        mainBox.set_max_children_per_line(self.config["maxOfficesPerColumn"])  #8
        mainBox.set_selection_mode(Gtk.SelectionMode.NONE)
        mainBox.set_column_spacing(self.config["officeBoxSpacing"])    #50
        mainBox.set_row_spacing(self.config["officeBoxSpacing"])    #20

        offices = ballot.offices
        for office in offices:
            officeClass = getattr(self.ballot, office)
            officeBox = LegacyOfficeBox(officeClass)
            officeBox.AVSCBB.connect("changed", self.getVotedCandidates)

            #self.pack_start(candidateBox, 0, 0, 0)
            mainBox.add(officeBox)

        hbox = Gtk.Box()
        backButton = Gtk.Button(label="Back")
        backButton.connect("clicked", self.goBack, orderedStack)
        submitButton = Gtk.Button(label="Submit")
        submitButton.connect("clicked", self.submitBallot, mainAVS, orderedStack)
        hbox.pack_start(backButton, False, False, 0)
        hbox.pack_start(submitButton, False, False, 10)

        box = Gtk.Box()
        box.pack_start(hbox, True, False, 0)

        """Hacks
        frame = Gtk.Frame()
        frame.set_label("Pick a candidate per office")
        frame.add(mainBox)
        mainBox.set_margin_top(10)
        mainBox.set_margin_bottom(20)
        mainBox.set_margin_left(10)
        mainBox.set_margin_right(10)
        mainBox = frame
        """

        self.pack_start(mainBox, True, False, 20)
        self.pack_end(box, True, False, 20)
        self.show_all()

        #horizontalContainerBox = Gtk.Box(spacing=20)
        #horizontalContainerBox.pack_start(mainContentBox, 1, 0, 20)

    def reset(self):
        for child in self.get_children():
            self.remove(child)

        self.ballot = None

    def goBack(self, backButton, orderedStack):
        dialog = Gtk.MessageDialog(self.get_toplevel(), None, Gtk.MessageType.QUESTION, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK), "Are you sure you want to discard this ballot?")
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.OK:
            orderedStack.previous(reset=True)

    def submitBallot(self, submitButton, mainAVS, orderedStack):
        orderedStack.next(self.ballot, mainAVS, orderedStack, reset=True)        #only ballot should be in here but meh

    def getVotedCandidates(self, AVSCBB):
        print()
        for office in self.ballot.offices:
            officeClass = getattr(self.ballot, office)
            print("{}: {}".format(officeClass.officeName, officeClass.votedCandidate))
        print()

####

class CandidateToggleButton(Gtk.ToggleButton):
    def __init__(self, candidate, picture_filename):
        Gtk.Button.__init__(self)
        #tooltip_text = centerText(candidate.name, candidate.party)
        #tooltip_text = tooltip_text[0] + "\n" + tooltip_text[1]
        tooltip_text = "{} [{}]".format(candidate.name, candidate.party)
        self.set_tooltip_text(tooltip_text)     #center this properly
        self.candidate = candidate

        contentBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        candidatePicture = Gtk.Image.new_from_file(str(PurePath(picture_filename)))
        #print(picture_filename)
        contentBox.pack_start(candidatePicture, True, False, 5)

        """#If names are really wanted
        candidateLabel = Gtk.Label(self.candidate.name)
        candidateLabel.set_line_wrap(True)
        candidateLabel.set_justify(Gtk.Justification.CENTER)
        contentBox.pack_end(candidateLabel, True, False, 0)
        """

        contentBox.set_hexpand(True)
        box = Gtk.Box()
        box.pack_start(contentBox, False, False, 5)
        self.set_size_request(126, 126)       #mainly needed for the label wrapping
        self.add(box)

class OfficeBox(Gtk.Box):
    def __init__(self, office, picturesFolder, picture_format=".jpg"):        #make dis take picture filename format fron a config; hardcoded to jpg rn
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.office = office

        candidateButtonsBox = Gtk.Box(spacing=10)       #officeBoxSpacing
        candidateButtonsBox.set_homogeneous(True)
        self.candidateButtons = []
        for candidate in self.office.candidateList:
            if candidate.office != self.office.officeName:
                print("Office mismatch. Skipping candidate", candidate.name)
                continue

            picture_filename = PurePath(picturesFolder, candidate.name + picture_format)
            candidateButton = CandidateToggleButton(candidate, picture_filename)
            candidateButton.connect("toggled", self.toggleCandidate,)
            self.candidateButtons.append(candidateButton)
            candidateButtonsBox.pack_start(candidateButton, False, False, 0)

        centerBox = Gtk.Box()
        centerBox.pack_start(candidateButtonsBox, True, False, 0)
        self.label = Gtk.Label(self.office.officeName)
        self.pack_start(self.label, False, False, 0)
        self.pack_start(centerBox, False, False,0)

    def toggleCandidate(self, candidateButton):    #move to ToggleCandidateButton and make it return candidate? idk
        candidate = candidateButton.candidate
        state = candidateButton.props.active
        otherCandidateButtons = [candidateBut for candidateBut in self.candidateButtons if candidateBut != candidateButton]
        if state:
            for candidateButton in otherCandidateButtons:
                candidateButton.set_active(False)
            self.office.voteCandidate(candidate)
        else:
            self.office.voteCandidate(None)

class AVSComboBoxText(Gtk.ComboBoxText):        #set_model should not be used acc documentation, but meh
    def __init__(self, entries, *args, placeholder_text=None, match_func=None, **kwargs):
        Gtk.ComboBoxText.__init__(self, has_entry=True, *args, **kwargs)

        if entries == None:
            entries = []

        entries.sort()      #should this be here or somewhere higher in the pipeline?
        for entry in entries:
            self.append_text(entry)

        completion = Gtk.EntryCompletion(inline_completion=False)       #Toggled to True for debug only
        completion.set_text_column(0)
        completion.set_minimum_key_length(1)
        completion.set_model(self.get_model())    #hardcoded static entries for now
        if match_func is not None:
            completion.set_match_func(match_func)

        entry = self.get_child()
        entry.set_placeholder_text(placeholder_text)
        entry.set_completion(completion)

    def updateOtherEntries(self, nameEntry, gradeEntry, sectionEntry, masterDB):       #Refactor so this can be used for other Gtk.Entry in the future
        student = nameEntry.get_active_text()

        grade, section = (None, None)
        if masterDB != None:
            grade, section = masterDB.getStudentInfo(student)

        if (grade == None) or (section == None):        #Is this necessary or annoying?
            gradeEntry.set_active(-1)
            gradeEntry.set_text("")
            sectionEntry.set_active(-1)
            sectionEntry.set_text("")

        for gradeLevel in gradeEntry.get_model():
            if  gradeLevel[0] == grade:
                gradeEntry.set_active_iter(gradeLevel.iter)

        for sectioni in sectionEntry.get_model():
            if  sectioni[0] == section:
                sectionEntry.set_active_iter(sectioni.iter)

    #Convenience wrapper functions
    def set_max_length(self, length):
        self.get_child().set_max_length(length)

    def set_text(self, text):
        self.get_child().set_text(text)

    def get_text(self):
        return self.get_child().get_text()

################

class AVSVoterInfoScreen(Gtk.Box):      #Prototype
    def __init__(self, mainAVS, orderedStack, *args, **kwargs):
        Gtk.Box.__init__(self, *args, **kwargs)
        #Make these into comboBoxes? or make submit only activate after all of them are properly filled
        #Completion for name and section (+ dat folder implementation?)

        names, grades, sections = (None, None ,None)
        masterDB = mainAVS.masterDB
        #if masterDB != None:        #This or just rely on masterDB's empty list return?
        names = masterDB.getAllNames()
        grades = masterDB.getAllGrades()
        sections = masterDB.getAllSections()

        self.nameEntry = AVSComboBoxText(names, placeholder_text="Surname, Firstname. M.I.", match_func=self.isInName)
        self.gradeEntry = AVSComboBoxText(grades, placeholder_text="Grade")       #make this only accept ints
        self.sectionEntry = AVSComboBoxText(sections, placeholder_text="Section")
        self.submitButton = Gtk.Button(label="Submit")

        #Make the placeholder text center
        self.gradeEntry.set_max_length(2)
        self.submitButton.connect("clicked", self.submitInfo, mainAVS, orderedStack)
        self.nameEntry.connect("changed", self.nameEntry.updateOtherEntries, self.gradeEntry, self.sectionEntry, mainAVS.masterDB)

        entriesBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        entriesBox.pack_start(self.nameEntry, False, False, 10)
        entriesBox.pack_start(self.gradeEntry, False, False, 10)
        entriesBox.pack_start(self.sectionEntry, False, False, 10)

        mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        mainBox.pack_start(entriesBox, False, False, 0)
        mainBox.pack_start(self.submitButton, False, False, 0)
        self.submitButton.set_margin_top(50)

        #Hacks For now
        frame = Gtk.Frame()
        frame.set_label("Voter Info")
        #frame.set_shadow_type(Gtk.ShadowType.IN)

        frame.add(mainBox)
        mainBox.set_margin_top(10)
        mainBox.set_margin_bottom(20)
        mainBox.set_margin_left(10)
        mainBox.set_margin_right(10)
        mainBox = frame
        ####

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox.pack_start(mainBox, True, False, 0)
        self.pack_start(vbox, True, False, 0)

    def run(self):
        pass

    def reset(self):
        self.nameEntry.set_text("")
        self.gradeEntry.set_text("")
        self.sectionEntry.set_text("")

    def isInName(self, completion, key, it, *user_data):        #maybe move this somewhere more general
        key = key.lower()
        entry = completion.get_model().get(it, 0)[0].lower()
        if key in entry:
            return True
        else:
            name = "{1} {0}".format(*entry.split(","))
            return key in name

    def submitInfo(self, submitButton, mainAVS, orderedStack):
        main_GUI = self.get_toplevel()
        name = self.nameEntry.get_text()
        grade = self.gradeEntry.get_text()
        section = self.sectionEntry.get_text()

        for field in (name, grade, section):        #beuify later
            if field in (None, (None, ), "", " "):
                dialog = Gtk.MessageDialog(main_GUI, None, Gtk.MessageType.ERROR, (Gtk.STOCK_OK, Gtk.ResponseType.OK), "Please fill in all fields")
                response = dialog.run()
                dialog.destroy()
                return

        ballot = None
        try:
            ballot = mainAVS.newVoterBallot(name, grade, section)
        except AVSDB.AVSDBErrors.AVSError as e:       #Move to handleError for reuse?
            dialog = Gtk.MessageDialog(main_GUI, None, Gtk.MessageType.ERROR, (Gtk.STOCK_OK, Gtk.ResponseType.OK), e.message)
            response = dialog.run()
            dialog.destroy()

            policy = e.policy
            if policy == AVSDB.AVSExceptionHandler.POLICY_ASK:
                ballot = main_GUI.askMainServer(mainAVS, e, name, grade, section)
                if ballot is None:
                    dialog = Gtk.MessageDialog(main_GUI, None, Gtk.MessageType.ERROR, (Gtk.STOCK_OK, Gtk.ResponseType.OK), "Server denied re-entry")
                    response = dialog.run()
                    dialog.destroy()
                    return
                orderedStack.next(ballot, mainAVS, orderedStack, reset=True)
        else:
            orderedStack.next(ballot, mainAVS, orderedStack, reset=True)

class AVSMainVotingScreen(Gtk.Box):     #Sort of Proto?
    def __init__(self, config, *args, **kwargs):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.config = config

    def run(self, ballot, mainAVS, orderedStack):
        self.ballot = ballot    #Should the ballot even be owned? The only addition to accessible data is the voter's info
        mainBox = Gtk.FlowBox()
        mainBox.set_orientation(Gtk.Orientation.VERTICAL)
        mainBox.set_min_children_per_line(3)
        mainBox.set_max_children_per_line(self.config["maxOfficesPerColumn"])
        mainBox.set_selection_mode(Gtk.SelectionMode.NONE)
        mainBox.set_column_spacing(self.config["officeBoxSpacing"])

        #InfoBar to inform voters that they can hover on the portraits to get the names of the candidates
        infoBar = Gtk.InfoBar()
        infoBar.get_content_area().add(Gtk.Label("Hover on a portrait to get the candidate's name. A selected candidate can be deselected by either clicking on another candidate of the same office or by clicking on the selected candidate again."))
        infoBar.set_message_type(Gtk.MessageType.INFO)
        infoBar.set_show_close_button(True)
        self.pack_start(infoBar, True, False, 0)

        offices = ballot.offices
        for office in offices:
            officeClass = getattr(self.ballot, office)
            officeBox = OfficeBox(officeClass, self.config["assetsFolder"], self.config["pictureFormat"])
            for candidateButton in officeBox.candidateButtons:
                candidateButton.connect("toggled", self.getVotedCandidates)

            #self.pack_start(candidateBox, 0, 0, 0)
            mainBox.add(officeBox)

        hbox = Gtk.Box()
        backButton = Gtk.Button(label="Back")
        backButton.connect("clicked", self.goBack, orderedStack)
        submitButton = Gtk.Button(label="Submit")
        submitButton.connect("clicked", self.submitBallot, mainAVS, orderedStack)
        hbox.pack_start(backButton, False, False, 0)
        hbox.pack_start(submitButton, False, False, 10)

        box = Gtk.Box()
        box.pack_start(hbox, True, False, 0)

        self.pack_start(mainBox, True, False, 20)
        self.pack_end(box, True, False, 20)
        self.show_all()

        #horizontalContainerBox = Gtk.Box(spacing=20)
        #horizontalContainerBox.pack_start(mainContentBox, 1, 0, 20)

    def reset(self):
        for child in self.get_children():
            self.remove(child)

        self.ballot = None

    def goBack(self, backButton, orderedStack):
        dialog = Gtk.MessageDialog(self.get_toplevel(), None, Gtk.MessageType.QUESTION, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK), "Are you sure you want to discard this ballot?")
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.OK:
            orderedStack.previous(reset=True)

    def submitBallot(self, submitButton, mainAVS, orderedStack):
        orderedStack.next(self.ballot, mainAVS, orderedStack, reset=True)        #only ballot should be in here but meh

    def getVotedCandidates(self, candidateButton):
        pass#self.ballot._spillBallot(self.ballot.offices)

class AVSConfirmationScreen(Gtk.Box):       #add voter info? idk
    def __init__(self, config, *args, **kwargs):
        Gtk.Box.__init__(self, *args, orientation=Gtk.Orientation.VERTICAL, **kwargs)
        self.config = config

    def run(self, ballot, mainAVS, orderedStack):      #very Proto; add "unvote" functionality as shorthand? probably nah
        mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        candidatesBox = Gtk.FlowBox(homogeneous=True)
        candidatesBox.set_orientation(Gtk.Orientation.VERTICAL)
        candidatesBox.set_min_children_per_line(1)
        candidatesBox.set_max_children_per_line(3)
        candidatesBox.set_selection_mode(Gtk.SelectionMode.NONE)
        candidatesBox.set_column_spacing(50)

        votedCandidates = []
        for office in ballot.offices:       #reused code here so maybe make dem modular?
            candidateBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            officeClass = getattr(ballot, office)
            candidate = officeClass.votedCandidate

            if candidate == None:       #add "You abstained from voting in:" instead
                continue    #candidateBox.pack_end(Gtk.Label(office + ": " + "---"), True, False, 0)
            elif self.config["legacyMode"]:
                candidateBox.pack_start(Gtk.Label(office + ": " + candidate.name), True, False, 0)
            else:
                candidatePicture = Gtk.Image.new_from_file(str(PurePath(self.config["assetsFolder"], candidate.name + self.config["pictureFormat"])))
                tooltip_text = centerText(candidate.name, candidate.party)
                tooltip_text = tooltip_text[0] + "\n" + tooltip_text[1]
                candidatePicture.set_tooltip_text(tooltip_text)

                candidateBox.pack_start(candidatePicture, True, False, 0)
                candidateBox.pack_end(Gtk.Label(office), True, False, 0)

            votedCandidates.append(candidateBox)

        if len(votedCandidates) == 0:
            mainBox.pack_start(Gtk.Label("It seems like You didn't vote for anyone!"), False, False, 0)
        else:
            mainBox.pack_start(Gtk.Label("In summary, here are the candidates you have chosen:"), False, False, 0)
            for candidate in votedCandidates:
                candidatesBox.add(candidate)

            mainBox.pack_start(candidatesBox, False, False, 0)
            candidatesBox.set_margin_top(50)

        backButton = Gtk.Button(label="Back")
        backButton.connect("clicked", self.goBack, orderedStack)
        submitButton = Gtk.Button(label="Submit")
        submitButton.connect("clicked", self.submitBallot, ballot, mainAVS, orderedStack)
        box = Gtk.Box()
        hbox = Gtk.Box()
        hbox.pack_start(backButton, False, False, 0)
        hbox.pack_start(submitButton, False, False, 10)
        box.pack_start(hbox, True, False, 0)
        mainBox.pack_start(box, False, False, 20)

        self.pack_start(mainBox, True, False, 0)
        self.show_all()

    def reset(self):
        for child in self.get_children():
            self.remove(child)

    def goBack(self, backButton, orderedStack):
        orderedStack.previous(run=False)

    def submitBallot(self, submitButton, ballot, mainAVS, orderedStack):
        main_GUI = self.get_toplevel()
        try:
            mainAVS.processBallot(ballot)
        except AVSDB.AVSDBErrors.AVSError as e:
            label = Gtk.Label(e.message)        #Too lazy to write a proper message; hack for now
            dialog = Gtk.MessageDialog(main_GUI, None, Gtk.MessageType.ERROR, (Gtk.STOCK_OK, Gtk.ResponseType.OK), e.message)
            response = dialog.run()
            dialog.destroy()

            voter = ballot.voter
            policy = e.policy
            if policy == AVSDB.AVSExceptionHandler.POLICY_ASK:
                ballot = main_GUI.askMainServer(mainAVS, e, voter.name, voter.grade, voter.section)
                dialog.destroy()
                if ballot is None:
                    dialog = Gtk.MessageDialog(main_GUI, None, Gtk.MessageType.ERROR, (Gtk.STOCK_OK, Gtk.ResponseType.OK), "Server denied re-entry.")
                    response = dialog.run()
                    dialog.destroy()
                    return

                orderedStack.next(ballot, mainAVS, orderedStack, reset=True)
        else:
            dialog = Gtk.MessageDialog(main_GUI, None, Gtk.MessageType.INFO, (Gtk.STOCK_OK, Gtk.ResponseType.OK), "Vote Incremented. Thanks for voting")
            response = dialog.run()
            dialog.destroy()

        orderedStack.go_to_page(1, reset=True)
        self.reset()

class OrderedStack(Gtk.Stack):      #Move to different class?; cleanup the visible_child_index situation; REDESIGN
    def __init__(self, *args, **kwargs):
        Gtk.Stack.__init__(self, *args, **kwargs)
        self.children = []      #just use get_children everytime?
        self.visible_child_index = 0    #use a child's name property property

    def add_named(self, widget, name):
        Gtk.Stack.add_named(self, widget, name)
        self.children.append(widget)

    def set_visible_child(self, widget, *data, **kwargs):     #Also overload it's _full and _named cousins; accept transitionType param for more flexibility
        Gtk.Stack.set_visible_child(self, widget)
        #self.children[self.children.index(widget)].run(*data, **kwargs)
        #self.visible_child_index = integrate in the future

    def next(self, *data, run=True, reset=False, **kwargs):       #make a base function for next, previous, and go_to_page?
        self.visible_child_index += 1
        if self.visible_child_index >= len(self.children):    #first thing to do in func to save memory?
            print("No next children")
            return
        if reset:
            self.children[self.visible_child_index].reset()
        if run:
            self.children[self.visible_child_index].run(*data, **kwargs)
        self.set_visible_child(self.children[self.visible_child_index], *data, **kwargs)
        #self.visible_child_index += 1

    def previous(self, *data, run=True, reset=False, **kwargs):
        self.visible_child_index -= 1    #merge to line 1?
        if self.visible_child_index < 0:
            print("No previous child")
            return
        if reset:
            self.children[self.visible_child_index].reset()
        if run:
            self.children[self.visible_child_index].run(*data, **kwargs)
        self.set_visible_child(self.children[self.visible_child_index], *data, **kwargs)

    def go_to_page(self, page, *data, run=True, reset=False, **kwargs):
        if page > len(self.children) or page < 0:
            print("Page(",  page, ")must be between 1 and", len(self.children))
            return
        page -= 1
        if reset:
            self.children[page].reset()
        if run:
            self.children[page].run(*data, **kwargs)
        self.set_visible_child(self.children[page], *data, **kwargs)
        self.visible_child_index = page

class ElectronicBallotWindow(Gtk.Window):
    def __init__(self, mainAVS, config):
        Gtk.Window.__init__(self, title="Saytek Electronic Ballot Voting System", border_width=20, deletable=False, window_position=Gtk.WindowPosition.CENTER)
        self.mainAVS = mainAVS
        self.config = config

        #Window manager hints; currenly does not work(i3)
        self.set_keep_above(True)
        self.fullscreen()    #except dis, dis work ebriwer

        self.mainStack = OrderedStack()
        self.mainStack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.mainStack.set_transition_duration(1000)

        voterInfoScreen = AVSVoterInfoScreen(self.mainAVS, self.mainStack)
        mainVotingScreen = (AVSLegacyMainVotingScreen if config["legacyMode"] else AVSMainVotingScreen)(self.config)
        confirmationScreen = AVSConfirmationScreen(self.config)

        self.mainStack.add_named(voterInfoScreen, "Voter Info")
        self.mainStack.add_named(mainVotingScreen, "Main Ballot")
        self.mainStack.add_named(confirmationScreen, "Confirmation Screen")
        self.mainStack.set_homogeneous(True)
        #Every mainStack member that might need to scrolled should be individually parented by a ScrolledWindow, but only the mainStack is scrolled for now to not introduce as many changes
        scroll = Gtk.ScrolledWindow()
        scroll.add(self.mainStack)
        self.add(scroll)#self.mainStack)
        #self.set_focus(None)    #Does not work for now; set_focus(None) is manually called in __main__ for now

    ####These are to be used by the class itself, or by its children
    def askMainServer(self, mainAVS, error, name, grade, section):      #Maybe move to the main window? idk
        dialog = Gtk.MessageDialog(self, None, Gtk.MessageType.INFO, (Gtk.STOCK_OK, Gtk.ResponseType.OK), "Asking server permission to re-enter. Awaiting server response...")
        response = dialog.run()
        voter = AVSDB.AVSPrimitives.Voter(name, grade, section)
        ballot = mainAVS.ask_error_handling(error, voter)
        dialog.destroy()

        return ballot

if __name__ == "__main__":
    import json
    import argparse
    from Core.AVS_Misc_Utilities import getOfficeCandidates, getPartyKeys, getNonPartyKeys, parseMasterList, getConfig, getCandidates
    parser = argparse.ArgumentParser(description="Make an instance of the Electric Ballot",prog="EAVS")
    parser.add_argument("candidates", nargs="?", help="a JSON file that holds the candidate list for the election")
    parser.add_argument("config", default="default.json", nargs='?', help="a JSON file used as config for the program. See Documentation for details(default:default.json)")
    args = parser.parse_args()

    """
    #here be hacks
    import getpass

    if args.pcNum == 0 or args.pcNum == "user":
        args.pcNum = getpass.getuser()[-1]
    if not args.pcNum.isnumeric():
        print("{} is not an int. defaulting to 2".format(args.pcNum))
        args.pcNum = 2

    print(args.pcNum)
    """

    config = getConfig(args.config)
    ui_config= config["ui_config"]
    offices = config["offices"]
    candidates = getCandidates(args.candidates, offices)
    officeCandidatesMaster = getOfficeCandidates(candidates)
    dbConfig = config["db_config"]
    pre_election = config["pre_election"]

    ####End of Config Setup###########################################################################

    masterCandidateList = parseMasterList(offices, officeCandidatesMaster)
    AVSexception_handler = AVSDB.AVSExceptionHandler({AVSDB.AVSDBErrors.HasAlreadyRegisteredError: AVSDB.AVSExceptionHandler.POLICY_ASK})
    mainAVS = AVSDB.AVSLogic(dbConfig["votes_db"], dbConfig["voter_db"], offices, masterCandidateList, AVSexception_handler, masterDBFile=dbConfig["master_db"], pre_election=pre_election)
    electionBallotMainWindow = ElectronicBallotWindow(mainAVS, ui_config)
    electionBallotMainWindow.show_all()
    electionBallotMainWindow.set_focus(None)
    electionBallotMainWindow.connect("delete-event",Gtk.main_quit)
    Gtk.main()
