#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo
MIT License
"""

import udi_interface
from enum import Enum
from typing import List
from nodes.observers.polyglotObserver import PolyglotObserver
from nodes.zone.ZoneNode import ZoneNode

LOGGER = udi_interface.LOGGER
Custom = udi_interface.Custom


class Drivers(Enum):
    numberRunning = "GV0"


'''
This is our Zone parent node. 
'''
class ZoneParentNode(udi_interface.Node):
    #------------- Node Definitions
    id = 'zoneParent'
    address='stations' 
    name='OpenSprinkler Stations'

    #shared observer
    polyObserver: PolyglotObserver

    #------------- Status Drivers
    drivers = [
            {'driver': Drivers.numberRunning.value, 'value': None, 'uom': 25},
            ]

    #------------- Data
    # holds all of our zone nodes
    list: List[ZoneNode] 
    currentQueue: int = None

    # Nodes/Node Holders

    
    def __init__(self, polyglot, polyObserver):
        LOGGER.info(' init')
        self.poly = polyglot
        self.polyObserver = polyObserver

        #Set initial values
        self.list = []
        
        # Add this node to ISY
        super(ZoneParentNode, self).__init__(polyglot, self.address, self.address, self.name)
        self.poly.addNode(self)
        

    
    #---------- Status Setters

    def setRunningProgramDriver(self, value: List[List[int]]):
        queued = 0
        for station in value:
            #do not add the station if the the program id is 0
            if station[0] == 0:
                continue
            queued += 1
        #only set the value if it has changed
        if self.currentQueue != None and self.currentQueue == queued:
            return
        self.currentQueue = queued
        self.setDriver(Drivers.numberRunning.value, queued, True, True)
    

    #---------- MQTT Observers


    #---------- Command  Observers


    #---------- Business Logic

    # @parm station lsit is an open sprinkler station list
    def equals(self, stationList):
        
        #get the list from the stationList Object
        newList = stationList.list
        #if list sizes are not different than the list has not changed
        if len(self.list) == len(newList):
            return

        #convert open sprinkler Stations to ZoneNodes
        self.list = []
        for station in stationList.list:
            zone = ZoneNode(self.poly, self.address, station, self.polyObserver)
            self.list.append(zone)