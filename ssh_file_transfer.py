#!/usr/bin/python
import os, stat
import paramiko
from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf


def on_tree_selection_changed2(selection):
    model, treeiter = selection.get_selected()
    if treeiter != None:
        print ("You selected", model[treeiter][0])

def populateFileSystemTreeStore2(self,treeStore, path, parent=None):
    itemCounter = 0
    # iterate over the items in the path
    for item in self.ftp.listdir_attr(path):
        # Get the absolute path of the item
        itemFullname = path+"/"+item.filename

        # Extract metadata from the item
        itemMetaData = self.ftp.stat(itemFullname)
        # Determine if the item is a folder
        itemIsFolder = stat.S_ISDIR(itemMetaData.st_mode)
        # Generate an icon from the default icon theme
        itemIcon = Gtk.IconTheme.get_default().load_icon("folder" if itemIsFolder else "empty", 22, 0)
        # Append the item to the TreeStore
        currentIter = treeStore.append(parent, [item.filename, itemIcon, itemFullname])
        # add dummy if current item was a folder
        if itemIsFolder: treeStore.append(currentIter, [None, None, None])
        #increment the item counter
        itemCounter += 1
    # add the dummy node back if nothing was inserted before
    if itemCounter < 1: treeStore.append(parent, [None, None, None])

def onRowExpanded2(treeView, treeIter, treePath):
    # get the associated model
    treeStore = treeView.get_model()
    # get the full path of the position
    newPath = treeStore.get_value(treeIter, 2)
    # populate the subtree on curent position
    populateFileSystemTreeStore2(treeStore, newPath, treeIter)
    # remove the first child (dummy node)
    treeStore.remove(treeStore.iter_children(treeIter))

def onRowCollapsed2(treeView, treeIter, treePath):
    # get the associated model
    treeStore = treeView.get_model()
    # get the iterator of the first child
    currentChildIter = treeStore.iter_children(treeIter)
    # loop as long as some childern exist
    while currentChildIter:
        # remove the first child
        treeStore.remove(currentChildIter)
        # refresh the iterator of the next child
        currentChildIter = treeStore.iter_children(treeIter)
    # append dummy node
    treeStore.append(treeIter, [None, None, None])

