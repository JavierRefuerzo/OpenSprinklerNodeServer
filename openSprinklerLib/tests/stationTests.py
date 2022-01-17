#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""


from multiprocessing.connection import wait
from objects.errors import Errors
from openSprinklerLib.station.station import Station
from openSprinklerLib.controller.credenital import Credential
from openSprinklerLib.controller.controller import Controller
from openSprinklerLib.programs.program import Program
from constants.params import Params
from openSprinklerLib.controller.VarsEnum import VarsEnum
import time


class StationTests:


    def __init__(self, creds: Credential):
        
        controller = Controller(creds, None)
        if controller.errors != None:
            print("Controller Error: " + controller.errors.text)
            

        controller.changeVariables(VarsEnum.resetAllStations.value, 0)

        stationList = controller.stationList
        if stationList.errors != None:
            print("Couild not get StationList: " + stationList.errors.text)
            exit()

        print("Stations: ")
        for station in stationList.list:
            station.statusListener = self.statusChangeCallback
            print("id: " + str(station.id) + ", name: " + station.name + ", status: " + str(station.status))

        station = stationList.list[0]


        #Station  command test
        station.setManualStationRun(enable=1, time=25)
        if station.errors != None:
            print("Error sending Command: " + station.errors.text)

        time.sleep(8)

        controller.getAll()

        #stationList.getStatus(creds, callback=statusChangeCallback)

        time.sleep(8)

        #stationList.getStatus(creds, callback=statusChangeCallback)

        controller.getAll()





        print("FINISHED !!!")


    def errorObserver(self, error: Errors):
        print("error: " + error.text)

    def statusChangeCallback(self, station: Station):
        print("-Station Changed: " + station.name + ", value: " + str(station.status) )
