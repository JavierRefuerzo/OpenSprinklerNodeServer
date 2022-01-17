#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""
from typing import Callable
from objects.errors import Errors
from openSprinklerLib.controller.endpoints import Endpoints
from openSprinklerLib.controller.openSprinklerRequest import OpenSprinklerRequest as Request


class Master:
    master1: bool
    master2: bool


class IgnoreRain:
    ignore: bool
    sensor1: bool
    sensor2: bool

class Station :
    errors: Errors = None

    #the parent openSprinkler controller
    controller = None

    id: int
    name: str
    status: int
    statusListener: Callable = None
    
    #TODO add these variables
    #ignoreRain: IgnoreRaing
    #master: Master

    def __init__(self, controller, id: int, name: str):
            self.controller = controller
            self.name = name
            self.id = id
            self.status = None

    def setstatus(self, status):
        self.status = status
        if self.statusListener != None:
            self.statusListener(self)


    def setManualStationRun(self, enable: int, time: int):
        self.errors = None
        commands = [('sid', self.id),('en', enable), ("t",time)]

        #station status request
        request = Request(credential=self.controller.creds, endpoint=Endpoints.manualStaionRun.value, commands=commands)
        if request.errors != None:
            self.errors = request.errors
            return