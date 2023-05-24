#!/usr/bin/env python3

import argparse

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from Core.AVS_Misc_Utilities import getConfig
import AVSGUI   #For da proto gui
import Network_bridge.AVS_Client as AVS_Client
from Network_bridge.ServerClient_Backends import JsonBackend

parser = argparse.ArgumentParser(description="Make an instance of the Electric Ballot",prog="EAVS")
parser.add_argument("config", default="default.json", nargs='?', help="a JSON file used as config for the program. See Documentation for details(default:default.json)")
parser.add_argument("pcNum", default=0, nargs='?', help="Pc Number identifier; used for naming the communicative json files")
args = parser.parse_args()

#here be hacks
import getpass

if args.pcNum == 0 or args.pcNum == "user":
    args.pcNum = getpass.getuser()
    #Routine to find out the last consecutive occurence of a digit starting from the last char
    start = -1
    for i in range(len(args.pcNum) - 1, -1, -1):
        if args.pcNum[i].isnumeric():
            start = i
        else:
            break

    args.pcNum = args.pcNum[start:]

if not args.pcNum.isnumeric():
    print("{} is not an int. defaulting to 2".format(args.pcNum))
    args.pcNum = 2

print("Client ID number: ", args.pcNum)

config = getConfig(args.config)
mainAVS = AVS_Client.ServerAVSBridge(args.pcNum, config["server_config"]["serverFolder"], JsonBackend(), config["db_config"]["master_db"])
ui_config = config["ui_config"]

win = AVSGUI.ElectronicBallotWindow(mainAVS, ui_config)
win.show_all()
win.connect("delete-event", Gtk.main_quit)
win.set_focus(None)
print()
Gtk.main()

