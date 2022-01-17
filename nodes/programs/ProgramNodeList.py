#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo
"""

from typing import List
import udi_interface
from nodes.programs.ProgramNode import ProgramNode

LOGGER = udi_interface.LOGGER
Custom = udi_interface.Custom

'''
Class which interfaces ProgramNodes and OpenSprinkler ProgramList
'''
class ProgramNodeList():

    list: List[ProgramNode]
    

    def __init__(self, polyglot, parent):
        self.polyglot = polyglot
        self.parent = parent
        self.list = []
        LOGGER.debug(' init')


    def equals(self, programList):
        
        #get the list from the stationList Object
        newList = programList.list
        #if list sizes are not different than the list has not changed
        #to od update creds here in case of change
        if len(self.list) == len(newList):
            return

        #Convert openSprinkler Programs to ProgramNodes
        self.list = []
        for program in programList.list:
            programNode = ProgramNode(self.polyglot, self.parent, program)
            programNode.addNodeToISY()
            self.list.append(programNode)