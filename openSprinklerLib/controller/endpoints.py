#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""
from enum import Enum

#enum zone status values
class Endpoints(Enum):
    stationNames = "jn"
    stationStatus = "js"
    manualStaionRun = "cm"
    progamData = "jp"
    startRunOnceProgram = "cr"
    manuallyStartProgram = "mp"
    changeControllerVariables = "cv"
    getStationVariables = "jc"
    getAll = "ja"
    changeProgramData = "cp"
    getOptions = "jo"