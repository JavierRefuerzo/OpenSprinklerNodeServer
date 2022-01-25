#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo
MIT License
"""

from typing import List
import udi_interface
from nodes.observers.polyglotObserver import PolyglotObserver
from nodes.zone.drivers import Drivers
from constants.params import Params as customParms
from openSprinklerLib.station.station import Station


LOGGER = udi_interface.LOGGER
Custom = udi_interface.Custom



'''
This is our Zone device node. 
'''
class ZoneNode(udi_interface.Node):
    #------------- Node Definitions
    id = "nodeDefZone"

    #------------- Status Drivers
    #these values are set by function before addNode
    drivers = []

    
    #------------- Data
    station: Station
    manualRunDurration: int = 0
    currentQueue: int = 0


    #shared observer
    polyObserver: PolyglotObserver


    def __init__(self, polyglot, parentAddress: str, station: Station, polyObserver:PolyglotObserver):
        LOGGER.info(' init')
        self.poly = polyglot

        #set custom params
        #self.Parameters = Custom(polyglot, 'customparams')

        #Set initial values
        self.station = station
       
        #change the station name to include stationId
        address = self.setAddress(stationId= station.id)

        # Add global observer
        self.polyObserver: PolyglotObserver = polyObserver
       
        self.setInitialDrivers()
        

        # Add this node to ISY
        super(ZoneNode, self).__init__(polyglot, parentAddress, address, station.name)
        self.poly.addNode(self)

        # OBSERVERS MUST BE ADDED AFTER addNode(self) or there may be a crash as the address does not exist
        self.station.statusListener = self.statusHandler
        self.station.controller.settings.ps_Listener.attach(self.setRunningProgramDriver)
         #self.polyObserver.attachCustomParamObserver(self.parameterHandler)
        self.polyObserver.customParams.attach(self.parameterHandler)
        # params = Custom(polyglot, 'customparams')
        # LOGGER.info('---------------------GET Custom params TEST ' + str(params))
        # if params != None:
        #     LOGGER.info('---------------------We have custom params')
        #     self.polyObserver.attachCustomParamObserver(self.parameterHandler)


        #set the station status values
        self.updateStationStatus()
        self.updateManulaRunDuration()

        # subscribe to the events we want
        self.setMqttObsevers()


    #---------- Unique Node Properties

    def setAddress(self, stationId: int) -> str:
        LOGGER.info('set address')
        self.address = 'zone_' + str(stationId)
        return self.address
    
    #---------- Status Setters

    def setInitialDrivers(self):
        LOGGER.info('set initial drivers')
        self.drivers = [
            {'driver': Drivers.status.value, 'value': self.station.status, 'uom': 25},
            {'driver': Drivers.manualRunDurration.value, 'value': self.manualRunDurration, 'uom': 57},
            {'driver': Drivers.queued.value, 'value': 0, 'uom': 2},
            ]

    def statusHandler(self, station):
        LOGGER.info('statusHandler')
        self.station = station
        self.updateStationStatus()

    def updateStationStatus(self):
        LOGGER.info('update station status')
        self.setDriver(Drivers.status.value, self.station.status, True, True)

    def updateManulaRunDuration(self):
        if self.manualRunDurration == None:
            LOGGER.info('manual run time is not set')    
            return
        self.setDriver(Drivers.manualRunDurration.value, self.manualRunDurration, True, True)


    def setRunningProgramDriver(self, value: List[List[int]]):
        queue = value[self.station.id][0]
        if queue > 0:
            queue = 1
        #only set the value if it has changed
        if self.currentQueue != None and self.currentQueue == queue:
            return
        self.currentQueue = queue
        self.setDriver(Drivers.queued.value, queue, True, True)

    #---------- MQTT Observers

    def setMqttObsevers(self):
        self.poly.subscribe(self.poly.CUSTOMPARAMS, self.parameterHandler)


    def parameterHandler(self, params):
        manualRunTime = params[customParms.manualRunTimeSeconds]
        if manualRunTime != None:
            self.manualRunDurration = manualRunTime
            self.updateManulaRunDuration()
            return
        LOGGER.info('manual run time is not set')    


    #---------- Command  Observers


    def startManualRun(self, val: int):
        LOGGER.info('startManualRun')
        if val is None:
            return
        self.station.setManualStationRun(val, self.manualRunDurration)
        if self.station.errors != None :
            LOGGER.info("Error sending command " + self.station.errors.text)


    def cmdManualRunTime(self, command):
        val = int(command.get('value'))
        if val == None:
            return
        self.manualRunDurration = val
        self.updateManulaRunDuration()

    def setOn(self, command):
        LOGGER.info('cmd 3')
        self.startManualRun(val=1)

    def setOff(self, command):
        LOGGER.info('cmd 4')
        self.startManualRun(val=0)

    
    commands = {
        "MANUAL_RUN_TIME": cmdManualRunTime,
        'DON': setOn,
        "DOF": setOff
    }

    #---------- Business Logic
        
  

   
  

    

    
   
            

    



