#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo
"""

from typing import List
import udi_interface
from nodes.zone.drivers import Drivers
from openSprinklerLib.programs.program import Program
from openSprinklerLib.controller.VarsEnum import VarsEnum
from enum import Enum



LOGGER = udi_interface.LOGGER
Custom = udi_interface.Custom

#enum for drivers
class Drivers(Enum):
    enabled = "GV0"
    queued = "GV1"

'''
This is our Zone device node. 
'''
class ProgramNode(udi_interface.Node):
    #nodeDefId
    id = "program"
    program: Program
    drivers = []
    
    currentQueue: int = None

    def __init__(self, polyglot, parentAddress: str, program: Program):
        LOGGER.info(' init')
        self.poly = polyglot
        self.program = program
        self.program.statusListener = self.statusHandler
        self.program.controller.settings.ps_Listener.attach(self.setRunningProgramDriver)
        #change the station name to include stationId
        address = self.setAddress(stationId= program.id)
        #set the station status
        self.updateEnabledStatus()
        #set station id
        super(ProgramNode, self).__init__(polyglot, parentAddress, address, program.name)

    

    def addNodeToISY(self):
        LOGGER.info('adding node to ISY. name: ' + self.name + ". Status:" + str(self.program.enabled))
        try:
            self.setInitialDrivers()
            self.poly.addNode(self)
            self.updateEnabledStatus()
        except Exception as e:
            LOGGER.error('Failed to create node:' + str(e))

    def setInitialDrivers(self):
        self.drivers = [
            {'driver': Drivers.enabled.value, 'value': self.program.enabled, 'uom': 2},
            {'driver': Drivers.queued.value, 'value': 0, 'uom': 2},
            ]

    def setAddress(self, stationId: int) -> str:
        self.address = 'program_' + str(stationId)
        return self.address

    def statusHandler(self, program):
        self.program = program
        self.updateEnabledStatus()

    # -------- Set drivers
    def updateEnabledStatus(self):
        self.setDriver(Drivers.enabled.value, self.program.enabled, True, True)

    def setRunningProgramDriver(self, value: List[List[int]]):
        queued = 0
        for station in value:
            program = station[0]
            #add 1 to the program index as the first program will be 1 and not running if zero
            if (program) == (self.program.id + 1):
                queued = 1
                break
        #only set the value if it has changed
        if self.currentQueue != None and self.currentQueue == queued:
            return
        self.currentQueue = queued
        self.setDriver(Drivers.queued.value, queued, True, True)

    # --------- Command Observers
    def runOnce(self, command):
        self.program.startRunOnce()

    def stopAll(self, command):
        self.program.changeVariables(VarsEnum.resetAllStations.value, 0)

    def enable(self, command):
        self.program.changeEnable(1)

    def disable(self, command):
        self.program.changeEnable(0)

    
    commands = {
        "MANUAL_RUN_ONCE": runOnce,
        "STOP_ALL_STATIONS": stopAll,
        "ENABLE": enable,
        "DISABLE": disable
    }




        

    

    