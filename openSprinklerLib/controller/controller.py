#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""
from tkinter.messagebox import NO
from typing import Callable
from objects.errors import Errors
from openSprinklerLib.controller.credenital import Credential
from openSprinklerLib.controller.settings import Settings
from openSprinklerLib.station.stationList import StationList
from openSprinklerLib.programs.programList import ProgramList
from nodes.controller.drivers import ErrorValues
from openSprinklerLib.controller.endpoints import Endpoints
from openSprinklerLib.controller.openSprinklerRequest import OpenSprinklerRequest as Request
from openSprinklerLib.station.stationStatus import StationStatus
from openSprinklerLib.controller.options import Options




class Controller :
    errors: Errors = None
    errorObserver: Callable = None

    creds: Credential
    stationList: StationList
    programList: ProgramList
    options: Options
    settings: Settings
    
    #TODO add these variables
    #ignoreRain: IgnoreRaing
    #master: Master

    def __init__(self, creds: Credential, errorObserver: Callable):
        self.creds = creds
        self.errorObserver = errorObserver
        self.stationList = StationList(self)
        self.programList = ProgramList(self)
        self.options = Options(self)
        self.settings = Settings(self)
        self.getAll()

    # ------ Setters with update listeners

    def setErrors(self, error: Errors):
        #set error to global
        self.errors = error
        #return if there is no observer
        if self.errorObserver == None:
            return
        #update observer    
        self.errorObserver(self.errors)
    
    '''
    Use these functions to set/clear errors so they are passed to observer function
    '''
    def clearError(self):
        noneError = Errors("none", code=ErrorValues.none.value)
        self.setErrors(noneError)

    

    # ---- Command functions


    def changeVariables(self, var: str, value: int):
        endpoint=Endpoints.changeControllerVariables.value
        commands = [(var, value)]

        #station status request
        request = Request(self.creds, endpoint, commands=commands)
        if request.errors != None:
            self.errors = request.errors
            return


     # ---- Get update

    def getAll(self):
        #clear errors
        self.clearError()
        #station status request
        request = Request(self.creds, Endpoints.getAll.value, commands=[])
        if request.errors != None:
            self.errors = request.errors
            return

        jsonSettings = request.jsonResponse['settings'] #controller variables
        jsonOptions = request.jsonResponse['options']
        jsonStations = request.jsonResponse['stations']
        jsonStatus = request.jsonResponse['status']
        jsonPrograms = request.jsonResponse['programs']

        # get options
        self.options.parse(jsonOptions)
        if self.options.errors != None:
            self.setErrors(self.options.errors)
            return

         # get settings
        self.settings.parse(jsonSettings)
        if self.settings.errors != None:
            self.setErrors(self.options.errors)
            return

        # get station list
        self.stationList.parse(jsonStations)
        if (self.stationList.errors != None):
            self.setErrors(self.stationList.errors)

        # get station values
        statusValues = StationStatus(self.stationList)
        statusValues.parse(jsonStatus, self.stationList)
        if statusValues.errors != None:
            self.setErrors(statusValues.errors)
            return
        self.stationList.list = statusValues.stationList.list       

        # get programs
        self.programList.parse(jsonPrograms)
        if self.programList.errors != None:
            self.setErrors(self.programList.errors)