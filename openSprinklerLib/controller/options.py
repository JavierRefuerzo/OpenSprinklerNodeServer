#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""

from nodes.controller.drivers import ErrorValues
from objects.LiveObject import LiveObject
from objects.errors import Errors
from openSprinklerLib.controller.openSprinklerRequest import OpenSprinklerRequest as Request
from openSprinklerLib.controller.endpoints import Endpoints



class Options:
    errors: Errors = None
    controller = None

    den_Listener: LiveObject
    
    fwv: int  #firmware version this app supports firmware greater than 219
   

    def __init__(self, controller):
        self.errors = None
        self.controller = controller
        #observers
        self.den_Listener = LiveObject()

    def makeRequest(self):
        request = Request(credential=self.controller.creds, endpoint=Endpoints.getOptions.value)
        if request.errors != None:
            self.errors = request.errors
            return
        self.parse(request.jsonResponse)    

    def parse(self, request):
        print("parse options")
        self.errors = None
        self.fwv = request['fwv']
        if self.fwv < 216:
            self.errors = Errors("Firmware 2.1.9 or greater required for this Node Server", ErrorValues.firmware.value)
        #this is the enabled flag it should be in controller variables also
        self.den_Listener.updateOnChange(request["den"])
