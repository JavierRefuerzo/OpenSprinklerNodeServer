#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""
from objects.errors import Errors
from typing import Callable
from openSprinklerLib.controller.credenital import Credential
from openSprinklerLib.controller.endpoints import Endpoints
from openSprinklerLib.controller.openSprinklerRequest import OpenSprinklerRequest as Request


class Program :
    errors: Errors = None

    #the parent openSprinkler controller
    controller = None

    id: int
    name: str
    enabled: int = None
    durration = []
    #weather adjustment
    statusListener: Callable = None
    
    #TODO add these variables
    #ignoreRain: IgnoreRaing
    #master: Master

    def __init__(self, controller, id: int, name: str):
            self.controller = controller
            self.name = name
            self.id = id
            self.status = None


    # ------------ Setters

    #use this to set enabled so observer is notified
    def setEnabled(self, enabled):
        # only update this value if it is not equal to the current value
        if self.enabled != None and self.enabled == enabled:
            return
        print("program enabled " + str(enabled)) 
        self.enabled = enabled
        if self.statusListener != None:
            self.statusListener(self)



    # ------------ Commands

    def startRunOnce(self):
        commands = [('pid', self.id)]
        #station status request
        request = Request(credential=self.controller.creds, endpoint=Endpoints.manuallyStartProgram.value, commands=commands)
        if request.errors != None:
            self.errors = request.errors
            return

    def changeVariables(self, var: str, value: int):
        self.controller.changeVariables(var=var, value=value)

    def changeEnable(self, value):
        commands = [("pid", self.id),('en', value)]
        #station status request
        request = Request(credential=self.controller.creds, endpoint=Endpoints.changeProgramData.value, commands=commands)
        if request.errors != None:
            self.errors = request.errors
            return