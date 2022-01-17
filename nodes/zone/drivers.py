#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""
from enum import Enum

#enum for drivers
class Drivers(Enum):
    status = "ST"
    manualRunDurration = "GV0"
    queued = "GV1"
