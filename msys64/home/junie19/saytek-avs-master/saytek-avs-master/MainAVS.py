#!/usr/bin/env python3
#DOESNTWORK: it seems that multiprocessing makes different contexes for each process, so in a way they do not share the same attributes
#Maybe add index/indentifier to listbox rows instead and use that to remove exception in stack (bc list.remove fails sometimes)
#TODO: find out why in every allow/block action in AVSExceptionHandlerGUI, padding is added
#Clean up and finalize mainAVSGUi
#add infoBar to alert on old config usage

import random       #For mock_data_propagation
#import multiprocessing
import subprocess   #for calling scale_images through cmd

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GObject, Gtk

from Core import AVSDBErrors

#The following are for config loading
from Core.AVS_Misc_Utilities import getOfficeCandidates, parseMasterList, getConfig, getCandidates
import Core.AVSDB as AVSDB
import Core.AVSDBErrors as AVSDBErrors
from Network_bridge.ServerClient_Backends import JsonBackend
import Network_bridge.AVS_Server as AVS_Server

class MockAEHStack(object):
    def __init__(self):
        self.stack = []
        #Separate attributes for each, or just in one stored in a dictionary
        self.on_append_callbacks = []
        self.on_block_callbacks = []
        self.on_allow_callbacks = []
        self.voter_num = 1

    """
    def start_propagation(self):
        print("Pre-propagation:", len(self.stack))
        #multiprocessing.Process(target=self.mock_data_propagation).start()
    """

    def mock_data_propagation(self):
        #print("MOCK PROPAGATION CALLED")
        while len(self.stack) < 10:
            if len(self.stack) < 10:
                name = "Voter %s" % self.voter_num
                exception = random.choice(self.mock_data_propagation.exceptions)
                data = {"Voter": name, "Exception": exception}
                self.add_to_queue(data)
                self.voter_num += 1
    mock_data_propagation.exceptions = [
        AVSDBErrors.HasAlreadyVotedError,
        AVSDBErrors.HasAlreadyRegisteredError,
        AVSDBErrors.VoterNotInDatabaseError,
        AVSDBErrors.VoterNotRegisteredError,
        AVSDBErrors.BallotError,
        AVSDBErrors.NoVoterInfo,
        AVSDBErrors.AVSDBError
    ]

    ##Add these to the AVSExceptionHandler class in AVSDB
    def add_to_queue(self, exception):
        self.stack.append(exception)
        for callback in self.on_append_callbacks:
            callback(exception)

    def allow_exception(self, exception):
        self.stack.remove(exception)
        for callback in self.on_allow_callbacks:
            callback(exception)

    def block_exception(self, exception):
        self.stack.remove(exception)
        for callback in self.on_block_callbacks:
            callback(exception)

    def register_callback(self, callback, signal="append"):
        if callback is None:
            return

        if signal == "append":
            self.on_append_callbacks.append(callback)
        elif signal == "allow":
            self.on_allow_callbacks.append(callback)
        elif signal == "block":
            self.on_block_callbacks.append(callback)

class MockAVSExceptionHandlerGUI(Gtk.Box):
    def __init__(self, aeh, *args, **kwargs):
        Gtk.Box.__init__(self, *args, orientation=Gtk.Orientation.VERTICAL, **kwargs)
        GObject.timeout_add(0, self.get_new_requests)
        self.aeh = aeh

        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.MULTIPLE)

        hbox = Gtk.Box()
        allow_button = Gtk.Button(label="Allow")
        allow_button.connect("clicked", self.allow_clicked)
        block_button = Gtk.Button(label="Block")
        block_button.connect("clicked", self.block_clicked)
        hbox.pack_start(block_button, False, False, 0)
        hbox.pack_start(allow_button, False, False, 0)

        self.pack_start(self.listbox, True, True, 0)
        self.listbox.set_margin_top(20)
        self.pack_start(hbox, False, False, 0)
        self.listbox.set_margin_top(20)
        self.listbox.add(Gtk.Label("Voter 0"))

    def update_listbox(self, data):
        self.listbox.add(Gtk.Label(data))
        self.listbox.show_all()


    def allow_clicked(self, button):
        selected_rows = self.listbox.get_selected_rows()
        if len(selected_rows) == 0:
            print("No Selected errors to allow.")
            return

        print("Here are the selected Rows:")
        for row in selected_rows:
            print(row.get_child().get_text())
            self.aeh.allow_exception(row.get_child().get_text())
            self.listbox.remove(row)

        print("Action: ALLOW")

    def block_clicked(self, button):
        selected_rows = self.listbox.get_selected_rows()
        if len(selected_rows) == 0:
            print("No Selected errors to block.")
            return

        print("Here are the selected Rows:")
        for row in selected_rows:
            print(row.get_child().get_text())
            self.aeh.block_exception(row.get_child().get_text())
            self.listbox.remove(row)

        print("Action: BLOCK")

    def get_new_requests(self):
        self.aeh.mock_data_propagation()
        GObject.timeout_add(1, self.get_new_requests)

class AVSExceptionListBoxRow(Gtk.ListBoxRow):
    def __init__(self, exception, *args, **kwargs):
        Gtk.ListBoxRow.__init__(self, *args, **kwargs)
        self.exception = exception
        exception_label = Gtk.Label(str(exception.voter) + ": " + exception.message)
        self.add(exception_label)
        exception_label.set_justify(Gtk.Justification.LEFT)
        exception_label.set_alignment(0, 0)

class AVSExceptionHandlerGUI(Gtk.Box):
    def __init__(self, aeh, mainAVS, *args, **kwargs):
        Gtk.Box.__init__(self, *args, orientation=Gtk.Orientation.VERTICAL, **kwargs)
        aeh.register_callback(self.add_exceptions, signal="append")

        self.exception_listbox = Gtk.ListBox()
        self.exception_listbox.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
        allow_button = Gtk.Button(label="Allow")
        block_button = Gtk.Button(label="Block")
        allow_button.connect("clicked", self.allow_selected_exceptions, aeh, mainAVS)
        block_button.connect("clicked", self.block_selected_exceptions, aeh, mainAVS)
        aeh.register_callback(self.remove_exceptions, signal="allow")
        aeh.register_callback(self.remove_exceptions, signal="block")
        scroll = Gtk.ScrolledWindow()
        scroll.add(self.exception_listbox)
        scroll.set_size_request(300, 500)   #Shouldn't be hardcoded; probably SCREENHEIGHT - 100px for height

        centering_box = Gtk.Box()
        centering_box.pack_start(allow_button, False, False, 0)
        centering_box.pack_start(block_button, False, False, 0)
        controls_box = Gtk.Box()
        controls_box.pack_start(centering_box, True, False, 0)

        centering_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        centering_vbox.pack_start(scroll, False, False, 0)
        centering_vbox.pack_start(controls_box, False, False, 0)
        controls_box.set_margin_bottom(10)
        controls_box.set_margin_top(10)
        centering_hbox = Gtk.Box()
        centering_hbox.pack_start(centering_vbox, True, False, 0)
        self.pack_start(centering_hbox, True, False, 0)

    def allow_selected_exceptions(self, allow_button, aeh, mainAVS):
        selected_rows = self.exception_listbox.get_selected_rows()
        for row in selected_rows:
            error = row.exception
            mainAVS.ask_error_handling(error, error.voter, ui_callback=lambda error, voter: True)
            #aeh.allow_exception(error, error.voter)

    def block_selected_exceptions(self, allow_button, aeh, mainAVS):
        selected_rows = self.exception_listbox.get_selected_rows()
        for row in selected_rows:
            error = row.exception
            mainAVS.ask_error_handling(error, error.voter, ui_callback=lambda error, voter: False)
            #aeh.block_exception(error, error.voter)

    def add_exceptions(self, exception):
        self.exception_listbox.add(AVSExceptionListBoxRow(exception))
        self.exception_listbox.show_all()

    def remove_exceptions(self, exception):
        for exceptionRow in self.exception_listbox.get_children():
            if exceptionRow.exception == exception:
                self.exception_listbox.remove(exceptionRow)
                break       #stops on first occurence of exception

        self.exception_listbox.show_all()

class MainControlGUI(Gtk.Box):
    def __init__(self, mainAVS,*args, **kwargs):     #assumes a mainAVS of type ClientAVSBridge
        Gtk.Box.__init__(self, *args, **kwargs)
        self.mainAVS = mainAVS
        self.stopped = True    #this shouldn't be in UI code, but eh
        start_button = Gtk.Button(label="Start election")
        stop_button = Gtk.Button(label="Stop election")
        start_button.connect("clicked", self.startElection)
        stop_button.connect("clicked", self.stopElection)

        controls_box = Gtk.Box()
        controls_box.pack_start(start_button, True, False, 0)
        controls_box.pack_start(stop_button, True, False, 0)
        controls_box.set_margin_bottom(10)
        frame = Gtk.Frame()
        frame.set_label("Main Functions")
        frame.add(controls_box)
        frame.set_valign(Gtk.Align.START)
        main_controls = frame

        exceptionGUI = AVSExceptionHandlerGUI(self.mainAVS.exceptionDispatcher, self.mainAVS)
        frame = Gtk.Frame()
        frame.set_label("Exception Handler")
        frame.add(exceptionGUI)
        frame.set_valign(Gtk.Align.START)
        exceptionGUI = frame
        #exceptionGUI.set_size_request(300, 500)

        self.pack_start(main_controls, True, True, 0)
        self.pack_start(exceptionGUI, True, True, 10)

    def set_AVS(self, avs):
        self.mainAVS = avs
        print("updated AVS instance (Config or Candidates was probably changed)")

    def startElection(self,button):
        self.stopped = False
        self.mainAVS.startElection()
        #TODO: make these separate processes/threads so they are not stalled when waiting for response
        self._electionLoop()

    def stopElection(self, button):
        self.stopped = True
        self.mainAVS.stopElection()
        return      #does nothing for now

    def _electionLoop(self):
            #print("exceptionDispatcher stack:", self.mainAVS.exceptionDispatcher.exception_stack)
            GObject.timeout_add(1, lambda: self.mainAVS.processNewVoters() if not self.stopped else None)
            GObject.timeout_add(1, lambda: self.mainAVS.processBallots() if not self.stopped else None)
            GObject.timeout_add(1, lambda: self.mainAVS.processErrors() if not self.stopped else None)
            GObject.timeout_add(1, self._electionLoop)

#Wrapper class that provides a basic Gtk.FileChooserButton for selecting directories
#As of writing, passing Gtk.FileChooserAction.SELECT_FOLDER to Gtk.FileChooserButton does not work
class FolderChooserButton(Gtk.Button):
    def __init__(self, *args, **kwargs):
        Gtk.Button.__init__(self, label="None", *args, **kwargs)
        self.connect("clicked", self.select_folder)

    def select_folder(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a folder", self.get_toplevel(),       #get_toplevel here assumes that toplevel is an actual window
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.set_label(dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def get_filename(self):
        filename = self.get_label()
        if filename == "None":
            return None
        else:
            return filename

class ScaleImagesDirectorySelectorGUI(Gtk.Box):
    def __init__(self, *args, **kwargs):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, *args, **kwargs)
        self.set_halign(Gtk.Align.START)

        source_box = Gtk.Box()
        source_button = FolderChooserButton()
        source_box.pack_start(Gtk.Label("Source:     "), False, False, 0)
        source_box.pack_start(source_button, False, False, 10)
        self.pack_start(source_box, False, False, 5)

        destination_box = Gtk.Box()
        destination_button = FolderChooserButton()
        destination_box.pack_start(Gtk.Label("Destination:"), False, False, 0)
        destination_box.pack_start(destination_button, False, False, 10)
        self.pack_start(destination_box, False, False, 5)

        scale_images_button = Gtk.Button(label="Resize images")
        scale_images_button.connect("clicked", self.resizeImages, source_button, destination_button)#lambda button: print("Resized images from", source_button.get_filename(), "and placed the resized images to", destination_button.get_filename()))
        self.pack_start(scale_images_button, False, False, 10)

    def resizeImages(self, button, source_button, destination_button):        #Hardcoded to scale_images.py for now and uses subprocess (i.e., it is ugly for now)
        source = source_button.get_filename()
        destination = destination_button.get_filename()

        if source is None:
            source = "./"

        if destination is None:
            destination = "resized_images"

        print("Source:", source, "Destination:", destination)
        if destination == source:
            dialog = Gtk.MessageDialog(self.get_toplevel(), None, Gtk.MessageType.QUESTION, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK), "The destination and the source are the same, which means the original files would be completely overwritten by the new ones. Albeit rare, this might also result to picture corruption. Continue?")
            response = dialog.run()
            dialog.destroy()
            if response == Gtk.ResponseType.CANCEL:
                return

        subprocess.run('cd "supplementary election scripts"; python3 -m scale_images "'  + source + '" "' + destination + '"', shell=True)
        #subprocess.run(["python3", "-m", "scale_images", source, destination])

        dialog = Gtk.MessageDialog(self.get_toplevel(), None, Gtk.MessageType.QUESTION, (Gtk.STOCK_OK, Gtk.ResponseType.OK), "Done resizing Images")
        response = dialog.run()
        dialog.destroy()

class ConfigFileSelectionGUI(Gtk.Box):
    def __init__(self, mainControlGUI, *args, **kwargs):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, *args, **kwargs)
        self.set_halign(Gtk.Align.START)

        candidates_box = Gtk.Box()
        self.candidates_button = Gtk.FileChooserButton("Select candidates file...", Gtk.FileChooserAction.OPEN)
        candidates_box.pack_start(Gtk.Label("Candidates file:"), False, False, 0)
        candidates_box.pack_start(self.candidates_button, False, False, 10)
        self.pack_start(candidates_box, False, False, 5)

        config_box = Gtk.Box()
        self.config_button = Gtk.FileChooserButton("Select config file...", Gtk.FileChooserAction.OPEN)
        config_box.pack_start(Gtk.Label("Config file:     "), False, False, 0)
        config_box.pack_start(self.config_button, False, False, 10)
        self.pack_start(config_box, False, False, 5)

        #Save previous configs so that they can be reverted to in case of an error
        self.candidates_button.previous =  self.candidates_button.get_filename()
        self.config_button.previous =  self.config_button.get_filename()

        self.candidates_button.connect("file-set", self.config_change, "Candidates file", mainControlGUI)
        self.config_button.connect("file-set", self.config_change, "Config file", mainControlGUI)

    def config_change(self, button, title, mainControlGUI):
        print(title, "changed to", button.get_filename())

        if not mainControlGUI.stopped:
            dialog = Gtk.MessageDialog(self.get_toplevel(), None, Gtk.MessageType.QUESTION, (Gtk.STOCK_OK, Gtk.ResponseType.OK), "Configs can't be changed while election is running. Please pause election first")
            response = dialog.run()
            dialog.destroy()
            #Hardcoded fallbacks in case either of the two previous configs are None
            self.candidates_button.set_filename(self.candidates_button.previous or "sample config/candidates/17-18_real.json")
            self.config_button.set_filename(self.config_button.previous or "sample config/config/avs_config.json")
            return      #config shouldn't be changed during election. Election must be first paused

        try:
            #Config loading routine and mainAVS instance creation copied from main
            config = getConfig(self.config_button.get_filename())     ############Hardcoded for now; select using a file chooser later
            candidates = getConfig(self.candidates_button.get_filename()) #######SAme here
            offices = config["offices"]
            officeCandidatesMaster = getOfficeCandidates(candidates)
            dbConfig = config["db_config"]
            serverConfig = config["server_config"]

            masterCandidateList = parseMasterList(offices, officeCandidatesMaster)
            AVSexception_handler = AVSDB.AVSExceptionHandler({AVSDB.AVSDBErrors.HasAlreadyRegisteredError: AVSDB.AVSExceptionHandler.POLICY_ASK})
            mainAVS = AVSDB.AVSLogic(dbConfig["votes_db"], dbConfig["voter_db"], offices, masterCandidateList, AVSexception_handler, masterDBFile=dbConfig["master_db"])
            new_AVS = AVS_Server.ClientAVSBridge(mainAVS, serverConfig["maxPCNum"], serverConfig["serverFolder"], JsonBackend())
        except BaseException as e:     #Generic catch-all except so that when anything was incorrect, we just don't change the mainAVS instance
            print("Either of the two configs supplied were invalid")        #Turn into a dialog or something that alerts the GUI admin
            dialog = Gtk.MessageDialog(self.get_toplevel(), None, Gtk.MessageType.QUESTION, (Gtk.STOCK_OK, Gtk.ResponseType.OK), "Configs supplied are invalid. The following error was thrown:" + str(e.args) + "\nThe election config and candidates are unchanged.")
            response = dialog.run()
            dialog.destroy()
            #Hardcoded fallbacks in case either of the two previous configs are None
            self.candidates_button.set_filename(self.candidates_button.previous or "sample config/candidates/17-18_real.json")
            self.config_button.set_filename(self.config_button.previous or "sample config/config/avs_config.json")
            return

        mainControlGUI.set_AVS(new_AVS)
        #Change is succesful, so previous configs must be updated
        self.candidates_button.previous = self.candidates_button.get_filename()
        self.config_button.previous = self.config_button.get_filename()

class GroupsSetupGUI(Gtk.Box):
    def __init__(self, *args,**kwargs):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, *args, **kwargs)

        box = Gtk.Box()
        box.pack_start(Gtk.Label("# of PCs"), False, False, 5)
        maxPcNum_entry = Gtk.SpinButton.new(Gtk.Adjustment(9.0, 0.0, 100.0, 1.0, 5.0, 0.0), 0.0, 0)
        maxPcNum_entry.set_numeric(True)
        box.pack_start(maxPcNum_entry, False, False, 0)
        setup_button  = Gtk.Button(label="Setup AVS groups/users")
        setup_button.connect("clicked", lambda button: self.setup(maxPcNum_entry.get_value_as_int()))

        self.pack_start(box, False, False, 5)
        self.pack_start(setup_button, False, False, 5)

    def setup(self, maxPcNum):
        dialog = Gtk.MessageDialog(self.get_toplevel(), None, Gtk.MessageType.QUESTION, (Gtk.STOCK_OK, Gtk.ResponseType.OK), "Please see the parent terminal of this window and type in the sudo password\nTODO: Make this ask through GUI (through PolKit or similar Technology)")
        response = dialog.run()
        dialog.destroy()

        subprocess.run('cd "supplementary election scripts"; bash setup.sh "'  + str(maxPcNum) + '"', shell=True)

        dialog = Gtk.MessageDialog(self.get_toplevel(), None, Gtk.MessageType.QUESTION, (Gtk.STOCK_OK, Gtk.ResponseType.OK), "Done setting up AVS groups and users.")
        response = dialog.run()
        dialog.destroy()

class MockMainAVS(object):
    def __init__(self, aeh):
        self.exceptionDispatcher = aeh
        self.stopped = False

    def startElection(self, button):
        self.stopped = False
        self._mockElection()

    def _mockElection(self):
        GObject.timeout_add(1, lambda : self.exceptionDispatcher.mock_data_propagation() if not self.stopped else None)
        GObject.timeout_add(1, self._mockElection)

    def stopElection(self, button):
        self.stopped = True
        return      #does nothing for now

if __name__ == "__main__":
    win = Gtk.Window()
    nb = Gtk.Notebook()
    bt1 = Gtk.Button(label="but1")
    bt2 = Gtk.Button(label="but2")
    bx1 = Gtk.Box(vexpand=False)
    bx2 = Gtk.Box(vexpand=False)

    """
    mockAEH = MockAEHStack()
    mainAVS = MockMainAVS(mockAEH)
    #lb = MockAVSExceptionHandlerGUI(mockAEH)
    #mockAEH.register_callback(lb.update_listbox, "append")
    #mockAEH.start_propagation()
    #test_AEHGUI = AVSExceptionHandlerGUI(mockAEH)
    """

    config = getConfig("sample config/config/avs_config.json")     ############Hardcoded for now; select using a file chooser later
    offices = config["offices"]
    candidates = getCandidates("sample config/candidates/17-18_real.json", offices) #######SAme here
    officeCandidatesMaster = getOfficeCandidates(candidates)
    dbConfig = config["db_config"]
    serverConfig = config["server_config"]
    pre_election = config["pre_election"]

    masterCandidateList = parseMasterList(offices, officeCandidatesMaster)
    AVSexception_handler = AVSDB.AVSExceptionHandler({AVSDB.AVSDBErrors.HasAlreadyRegisteredError: AVSDB.AVSExceptionHandler.POLICY_ASK})
    mainAVS = AVSDB.AVSLogic(dbConfig["votes_db"], dbConfig["voter_db"], offices, masterCandidateList, AVSexception_handler, masterDBFile=dbConfig["master_db"], pre_election=pre_election)
    serverAVS = AVS_Server.ClientAVSBridge(mainAVS, serverConfig["maxPCNum"], serverConfig["serverFolder"], JsonBackend())

    mainAVSGUI = MainControlGUI(serverAVS)

    bx1.pack_start(ScaleImagesDirectorySelectorGUI(), False, False, 0)
    bx1.pack_start(ConfigFileSelectionGUI(mainAVSGUI), False, False, 0)
    bx1.pack_start(GroupsSetupGUI(), False, False, 0)
    bx1.pack_start(bt1, True, False, 0)
    bx2.pack_start(bt2, True, False, 0)
    bt1.set_hexpand(False)
    bt1.set_vexpand(False)
    bt2.set_hexpand(False)
    bt2.set_vexpand(False)

    nb.add(bx1)
    nb.add(bx2)
    #nb.add(lb)
    #nb.add(test_AEHGUI)
    nb.add(mainAVSGUI)
    #nb.popup_enable()
    win.add(nb)
    win.show_all()
    win.connect("delete-event", Gtk.main_quit)

    Gtk.main()
