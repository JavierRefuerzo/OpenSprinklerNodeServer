#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""

from nodes.controller.drivers import ErrorValues
from objects.errors import Errors
from openSprinklerLib.controller.endpoints import Endpoints
from openSprinklerLib.controller.openSprinklerRequest import OpenSprinklerRequest as Request





class StationStatus :

    errors: Errors = None
    stationList = None
    hasChanged: bool
    
    def __init__(self, stationList):

        self.stationList = stationList
        self.hasChanged = False
        # #guard
        # if self.stationList == None:
        #     self.errors = Errors("Station list is null", code=ErrorValues.checkLogs.value)
        #     return

        # #station status request
        # request = Request(credential=controller.creds, endpoint=Endpoints.stationStatus.value)
        # if request.errors != None:
        #     self.errors = request.errors
        #     return

        # self.parse(request)
 
    def request(self, controller):
        #guard
        if self.stationList == None:
            self.errors = Errors("Station list is null", code=ErrorValues.checkLogs.value)
            return

        #station status request
        request = Request(credential=controller.creds, endpoint=Endpoints.stationStatus.value)
        if request.errors != None:
            self.errors = request.errors
            return

        self.parse(request.jsonResponse)


    def parse(self, request, stationList):
        self.stationList = stationList
        self.errors = None
        intStatusList = request['sn']
        #intNumberOfStations = request.jsonResponse['nstations']

        #guard
        if intStatusList == None:
            self.errors = Errors("Station status list is null", code=ErrorValues.checkLogs.value)
            return


        stations = self.stationList.list

        # this will be true for getAllfunction calling parser
        if self.stationList == None:
            self.stationList = stationList

        #guard
        if len(stations) != len(intStatusList):
            self.errors = Errors("Number of stations does not match number of station values: "+ str(len(stations)) + ":" + str(len(intStatusList)), code=ErrorValues.checkLogs.value)
            return


        #create station objects and add to list
        for index, station in enumerate(stations):
            intStatus = intStatusList[index]

            if station.status != None:
                if station.status == intStatus:
                    #value has not changed
                    continue
                
                    
            station.setstatus(intStatus)

