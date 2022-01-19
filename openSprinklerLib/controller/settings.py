#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""

from typing import List
from nodes.controller.drivers import ErrorValues
from objects.LiveObject import LiveObject
from objects.errors import Errors
from openSprinklerLib.controller.openSprinklerRequest import OpenSprinklerRequest as Request
from openSprinklerLib.controller.endpoints import Endpoints


#controller Variables
class Settings:

    errors: Errors = None

    rd_Listener: LiveObject
    sn1_Listener: LiveObject
    sn2_Listener: LiveObject
    ps_Listener: LiveObject


    def __init__(self, controller):
        self.errors = None
        self.controller = controller
        #observers
        self.rd_Listener = LiveObject()
        self.sn1_Listener = LiveObject()
        self.sn2_Listener = LiveObject()
        self.ps_Listener = LiveObject()

    def makeRequest(self):
        request = Request(credential=self.controller.creds, endpoint=Endpoints.getStationVariables.value)
        if request.errors != None:
            self.errors = request.errors
            return
        self.parse(request.jsonResponse)    

    def parse(self, request):
        print("parse options")
        self.errors = None
        #rain delay
        self.rd_Listener.updateOnChange(request['rd'] )
        # sensor 1 status
        if "sn1" in request:
            self.sn1_Listener.updateOnChange(request["sn1"])
        # sensor 2 status
        if "sn2" in request:
            self.sn2_Listener.updateOnChange(request["sn2"])
        #station status
        self.ps_Listener.updateOnChange(request["ps"])
        # ps has an array of arryas. one array for each station each array has 3 ints [0,0,0] the first it the program which started the station
        # The first number is the program number, or 99 is for manual run, or 254 is for run once program
        # The second number is the remaining water time in seconds
        # The third number is the start time
        # we can use this to tell if a program is running i.e. first index of a station, and if a station is queued i.e has time remaining


