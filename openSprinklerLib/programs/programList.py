#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""

from venv import create
from objects.errors import Errors
from openSprinklerLib.controller.endpoints import Endpoints
from openSprinklerLib.programs.program import Program
from typing import List

from openSprinklerLib.controller.openSprinklerRequest import OpenSprinklerRequest as Request




class ProgramList :

    errors: Errors = None
    list: List[Program] = []
    controller = None
    
    def __init__(self, controller):
        self.controller = controller


    def getProgramData(self):
        request = Request(credential=self.controller.creds, endpoint=Endpoints.progamData.value)
        if request.errors != None:
            self.errors = request.errors
            return
        self.parse(request.jsonResponse)    
        
    
    def parse(self, request):
        print("parse programs")
        self.errors = None
        json = request['pd']

        if len(json) != len(self.list):
            print("list size not equal")
            self.createProgramList(request)

        for index, data in enumerate(json):

            program = self.list[index]

            flag = data[0]
            #days0 = data[1]
            #days1 = data[2]
            #startTimesArray = data[3]
            program.durration = data[4]
            program.name = data[5]

            
            #Test to view convert flag to bytes
            #flag = 10
            #flagBytes = bin(flag)
            #print("program flag bytes: " + flagBytes) 

            
            #get first bit
            bit = flag&1
            program.setEnabled(bit)
            print("program enabled bytes" + str(flag) +". bit One: " + str(bit)) 
    

    #program creation is not needed in most cases so this should only happen on inital starup or if number of programs changed
    def createProgramList(self, request):
        json = request['pd']

        for index, data in enumerate(json):
            name = data[5]
            program = Program(controller=self.controller, id= index, name=name)
            self.list.append(program)
            
        print("created programs: " + str(len(self.list)))