#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""
from enum import Enum


#enum for drivers
class VarsEnum(Enum):
    resetAllStations = "rsn"
    reboot = "rbt"
    enableSystem = "en"
    setRainDelay = "rd"
    #re
    #ap
    #update