#!/usr/bin/env bash

setup_groups() {
    local max_pc="$1"
    sudo adduser --system avsserver
    sudo addgroup avs

    i=1
    while [ $i -le $max_pc ]
    do
        username=avspc$i
        echo $username
        echo "Creating user"
        sudo adduser $username
        echo "Adding user to avs group"
        sudo adduser $username avs
        echo
        i=$((i+1))
    done
}

setup_permissions() {
    #Set avs directory's owner and group to avsserver and avs respectively
    #Currently relies on the hardcoded setup that setup.sh is found one level into the avs directory
    local avs_directory="$1"
    if [[ $avs_directory != */ ]]
    then
        avs_directory=$avs_directory/
    fi
    avs_directory="$avs_directory"
    sudo chown -R avsserver:avs $avs_directory
    #Sets avs_directory permissions as follows:
    #   Owner(avsserver): rwx
    #   Group(avs): rx
    #   Others: No permissions
    sudo chmod 750 $avs_directory

    #Set fine-grained permissions for each file in avs directory
    #Currently relies on hardcoded filenames
    #Only admin (avsserver) should access scripts under this
    sudo chmod -R 700 $avs_directory"supplementary election scripts/"

    #Only the server and client can have access to the dependency modules
    #but for security purposes, only the server has the permission to modify them
    for folder in Network_bridge Core
    do
        sudo chmod 750 $avs_directory$folder
    done

    #Only server should have any access to MainAVS and AVSServer
    for file in MainAVS.py AVSServer.py
    do
        sudo chmod 700 $avs_directory$file
    done

    #The rest, AVSGUI and AVSClient, should be accessible only by the server and clients
    #Again, for security purposes, files cannot be modified by clients
    for file in AVSGUI.py AVSClient.py
    do
        sudo chmod 750 $avs_directory$file
    done
}

[ $# -gt 2 ] && { echo "Usage: $0 maxPcNum avs_directory"; exit 1; }
[ $# -eq 2 ] && { avs_directory="$2"; }
[ $# -eq 1 ] && { echo "No avs_directory given. defaulting to the hardcoded path (When launched from supplementary scrips)"; avs_directory=".././";}
[ $# -eq 0 ] && { echo "Usage: $0 maxPcNum avs_directory"; exit 1; }
max_pc="$1"

echo "Creating users"
setup_groups $max_pc
echo
echo
echo "Setting up permissions"
setup_permissions $avs_directory
echo "Done setting up permissions"
