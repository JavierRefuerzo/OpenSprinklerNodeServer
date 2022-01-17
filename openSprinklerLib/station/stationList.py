#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""

from objects.errors import Errors
from openSprinklerLib.controller.endpoints import Endpoints
from typing import List
from openSprinklerLib.station.station import Station
from openSprinklerLib.station.stationStatus import StationStatus
from openSprinklerLib.controller.openSprinklerRequest import OpenSprinklerRequest as Request




class StationList :

    errors: Errors = None
    list: List[Station] = []
    controller = None
    
    def __init__(self, controller):
        self.controller = controller

    def makeRequest(self):
        #station names request
        request = Request(credential=self.controller.creds, endpoint=Endpoints.stationNames.value)
        if request.errors != None:
            self.errors = request.errors
            return

        self.parse(request.jsonResponse)

          
    def parse(self, request):
        self.errors = None
        jsonNamesList = request['snames']

        if len(jsonNamesList) != len(self.list):
            print("Number of stations does not match "+ str(len(jsonNamesList)) + ":" + str(len(self.list)))
            self.list = self.createStationList(request)

        #create station objects and add to list
        for index, name in enumerate(jsonNamesList):
            station = self.list[index]
            station.name = name
            #self.list.append(station)
    
    #station creation is not needed in most cases so this should only happen on inital starup or if number of stations changed
    def createStationList(self, request) -> List:
        newList = []
        jsonNamesList = request['snames']
        for index, name in enumerate(jsonNamesList):
            station = Station(controller=self.controller, id=index,name=name)
            newList.append(station)
        return newList
    

