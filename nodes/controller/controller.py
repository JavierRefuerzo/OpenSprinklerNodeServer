#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""
from typing import Callable, List, final
import udi_interface
from nodes.controller.drivers import Drivers
from nodes.controller.drivers import StatusValues
from nodes.controller.drivers import ErrorValues
from objects.errors import Errors
from nodes.zone.ZoneParentNode import ZoneParentNode
from openSprinklerLib.controller.VarsEnum import VarsEnum
from openSprinklerLib.controller.controller import Controller as OpenSprinkler
from nodes.programs.ProgramNodeList import ProgramNodeList
from openSprinklerLib.controller.credenital import Credential
from nodes.observers.polyglotObserver import PolyglotObserver


LOGGER = udi_interface.LOGGER
Custom = udi_interface.Custom



'''
Controller 
'''
class Controller(udi_interface.Node):
    # Node Definitions
    id = 'ctl'
    address='opensprinkler' 
    name='OpenSprinkler'

    # Status Drivers
    drivers = [
            {'driver': Drivers.status.value, 'value': StatusValues.true.value, 'uom': 2},
            {'driver': Drivers.error.value, 'value': ErrorValues.none.value, 'uom': 25},
            {'driver': Drivers.controllerEnabled.value, 'value': StatusValues.false.value, 'uom': 2},
            {'driver': Drivers.rainDelay.value, 'value': StatusValues.false.value, 'uom': 2},
            {'driver': Drivers.sensor1.value, 'value': StatusValues.false.value, 'uom': 2},
            {'driver': Drivers.sensor2.value, 'value': StatusValues.false.value, 'uom': 2},
            {'driver': Drivers.runningProgram.value, 'value': 0, 'uom': 25},
            ]
    

    # Data
    openSprinkler: OpenSprinkler = None
    errorCode: int = ErrorValues.none.value
    customParamsHandlers: List[Callable] = []
    currentProgram: int = None

    # Nodes/Node Holders
    zoneParent: ZoneParentNode
    programList: ProgramNodeList

    #shared observer
    polyObserver: PolyglotObserver

    
    def __init__(self, polyglot):
        super(Controller, self).__init__(polyglot, self.address, self.address, self.name)   
        
        self.poly = polyglot
        self.polyObserver = PolyglotObserver(self.poly)

        #set custom params
        self.Parameters = Custom(polyglot, 'customparams')

        #Set initaial status 
        self.setStatus(statusEnum=StatusValues.true)

        # start processing events and create or add our controller node
        self.poly.ready()
        
        # Add this node to ISY
        self.poly.addNode(self)

        #Create objects which hold child nodes
        self.zoneParent = ZoneParentNode(self.poly, self.polyObserver)
        self.programList = ProgramNodeList(self.poly, self.address)

        # subscribe to the events we want
        self.setMqttObsevers()
        self.observeShared()

        #this should be moved out of this class and into an observer model
        #test_connect = connect.Connect(self.poly, controller=self)




    #---------- Status Setters

    def setStatus(self, statusEnum: StatusValues):
        self.setDriver(Drivers.status.value, statusEnum.value, True, True)

    def setControllerEnabled(self, value: int):
        self.setDriver(Drivers.controllerEnabled.value, value, True, True)

    def setRainDelayDriver(self, value: int):
        self.setDriver(Drivers.rainDelay.value, value, True, True)

    def setSensorOneDriver(self, value: int):
        self.setDriver(Drivers.sensor1.value, value, True, True)
    
    def setSensorTwoDriver(self, value: int):
        self.setDriver(Drivers.sensor2.value, value, True, True)

    def setRunningProgramDriver(self, value: List[List[int]]):
        final = 0
        for station in value:
            program = station[0]
            if program > final:
                final = program
        #only set the value if it has changed
        if self.currentProgram != None and self.currentProgram == final:
            return
        self.currentProgram = final
        self.setDriver(Drivers.runningProgram.value, final, True, True)

    def setError(self, error: Errors):
        #only update error code if it has changed
        if self.errorCode == error.code:
            return
        LOGGER.info('setError: ' + error.text)
        self.errorCode = error.code
        self.setDriver(Drivers.error.value, error.code, True, True)
        # set/remove notices
        if self.errorCode == ErrorValues.none.value:
            self.poly.Notices.clear()
        elif self.errorCode == ErrorValues.firmware.value:
            self.poly.Notices['firmware'] = 'OpenSprinkler Firmware Update Required to use this Node Server. Minimum firmware supported is 2.1.9. Please be sure to backup open sprinkler before upgrading firmware as you settings will be removed! https://openthings.freshdesk.com/support/home see User Manuals and select your hardware 3.x or 2.x'



    #---------- Shared Observer
    def observeShared(self):
        self.polyObserver.stop.attach(self.stop)
        self.polyObserver.customParams.attach(self.parameterHandler)
        self.polyObserver.polls.attach(self.poll)



    #---------- MQTT Observers

    def setMqttObsevers(self):
        self.poly.subscribe(self.poly.START, self.start, self.address)
        #other mqtt subsribe functions in shared observer
    
    def stop(self):
        LOGGER.info(' stop')
        self.setStatus(statusEnum=StatusValues.false)
        self.poly.stop()

    def start(self):
        LOGGER.info(' start called')
        self.poly.setCustomParamsDoc()
        self.poly.updateProfile()

    def parameterHandler(self, params):
        self.Parameters.load(params)
        #LOGGER.info('---------------------GET Custom params TEST ' + str(self.Parameters))
        #self.polyObserver.updateCustomParam(params)

    def poll(self, polltype):
        if 'shortPoll' in polltype:
            self.getOpenSprinklerStatus()
        # if 'longPoll' in polltype:
        #     self.updateStatus()


    #---------- Command  Observers

    def stopAll(self, command):
        self.openSprinkler.changeVariables(VarsEnum.resetAllStations.value, 0)

    def reboot(self, command):
        self.openSprinkler.changeVariables(VarsEnum.reboot.value, 1)

    def setRainDelay(self, command):
        val = int(command.get('value'))
        if val == None:
            return
        self.openSprinkler.changeVariables(VarsEnum.setRainDelay.value, val)    

    def enable(self, command):
        self.openSprinkler.changeVariables(VarsEnum.enableSystem.value, 1)

    def disable(self, command):
        self.openSprinkler.changeVariables(VarsEnum.enableSystem.value, 0)

    #Set Command Observers
    commands = {
            "RAIN_DELAY": setRainDelay,
            "STOP_ALL_STATIONS": stopAll,
            "REBOOT": reboot,
            "ENABLE": enable,
            "DISABLE": disable
        }


   
#---------- Business Logic

    def getOpenSprinkler(self):
        LOGGER.info('makeRequest')
        # get credentials and set/remove notices
        credential = Credential(params=self.Parameters)
        if credential.errors != None:
            LOGGER.info('Credential Error: ' + credential.errors.text)
            self.poly.Notices['credentials'] = 'Please set or check open sprinkler password and IP Address'
            self.setError(credential.errors)
            return
        

        self.openSprinkler = OpenSprinkler(credential, self.setError)
        #openSprinkler will send a 'none error' for the controller node, so lets not set openSprinkler to NONE
        if (self.openSprinkler.errors != None and self.openSprinkler.errors.code != ErrorValues.none.value):
            LOGGER.info('openSprinkler Error: ' + self.openSprinkler.errors.text)
            #error check not needed as error observable passed into OpenSprinkler
            self.openSprinkler = None
            return
        
        # add observers
        self.openSprinkler.options.den_Listener.attach(self.setControllerEnabled)
        self.openSprinkler.settings.rd_Listener.attach(self.setRainDelayDriver)
        self.openSprinkler.settings.sn1_Listener.attach(self.setSensorOneDriver)
        self.openSprinkler.settings.sn2_Listener.attach(self.setSensorTwoDriver)
        self.openSprinkler.settings.ps_Listener.attach(self.setRunningProgramDriver)
        self.openSprinkler.settings.ps_Listener.attach(self.zoneParent.setRunningProgramDriver)

        #these are new values so they must be inserted
        self.zoneParent.equals(self.openSprinkler.stationList)
        self.programList.equals(self.openSprinkler.programList)


    def getOpenSprinklerStatus(self):
        if self.openSprinkler == None:
            self.getOpenSprinkler()
            return
        self.openSprinkler.getAll()
        self.zoneParent.equals(self.openSprinkler.stationList)
        if self.openSprinkler.errors != None:
            self.setError(self.openSprinkler.errors)
            return
