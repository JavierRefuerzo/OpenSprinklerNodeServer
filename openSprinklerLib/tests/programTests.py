#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""


from multiprocessing.connection import wait
from nodes.controller.drivers import ErrorValues
from openSprinklerLib.station.station import Station
from openSprinklerLib.controller.credenital import Credential
from openSprinklerLib.controller.controller import Controller
from openSprinklerLib.programs.program import Program
from constants.params import Params
from openSprinklerLib.controller.VarsEnum import VarsEnum
import time


class ProgramTests:


    def __init__(self, creds: Credential):
        

        controller = Controller(creds, self.errorObserver)
        if controller.errors != None and controller.errors.code != ErrorValues.none.value:
            print("Controller Error: " + controller.errors.text)
            return
            

        controller.changeVariables(VarsEnum.resetAllStations.value, 0)
        controller.settings.rd_Listener.attach(self.rainDelayCallback)

        controller.changeVariables(VarsEnum.setRainDelay.value, 5)    

        #program TEst
        programList = controller.programList
        if programList.errors != None:
            print("Couild not get StationList: " + programList.errors.text)
            exit()

        print("Programs: ")
        testProgram = None
        for program in programList.list:
            if testProgram == None:
                testProgram = program
            program.statusListener = self.programChangeCallback
            print("id: " + str(program.id) + ", name: " + program.name + ", status: " + str(program.enabled) + "durration: " + str(program.durration))

        # program test
        print(" -- start test program")

        # sent enabled
        print(" -- set enabled")
        testProgram.changeEnable(1)
        # wait
        print(" -- wait")
        time.sleep(8)
        # get status
        print(" -- get status values")
        controller.getAll()
        print(" -- wait")
        time.sleep(8)
        # disable
        print(" -- set disabled")
        testProgram.changeEnable(0)
        # wait
        print(" -- wait")
        time.sleep(8)
        # get status
        print(" -- get status values")
        controller.getAll()

        print("FINISHED !!!")



    def errorObserver(self, error):
        print("error: " + error.text)


    def programChangeCallback(self, program: Program):
        print("-Program Changed: " + program.name + ", value: " + str(program.enabled) )

    def rainDelayCallback(self, value):
        print("-raindelay " + str(value))


