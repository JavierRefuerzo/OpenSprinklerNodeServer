#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""
from typing import Any, Callable, List
import udi_interface

from objects.LiveObject import LiveObject

LOGGER = udi_interface.LOGGER





class PolyglotObserver :
    
    #polyglot
    poly = None

    # Observed objects
    customParams: LiveObject
    start: LiveObject
    stop: LiveObject
    polls: LiveObject
    
    #customParamObserverList: List[Callable]
    
    
    def __init__(self, poly):
        self.poly = poly

        #------------set initial Data

        # observed objects
        self.customParams = LiveObject()
        self.stop = LiveObject()
        self.polls = LiveObject()

        # observe mqtt
        self.setMqttObsevers()


        
     #---------- MQTT Observers

    def setMqttObsevers(self):
        self.poly.subscribe(self.poly.STOP, self.stop.update)
        self.poly.subscribe(self.poly.CUSTOMPARAMS, self.customParams.update)
        self.poly.subscribe(self.poly.POLL, self.polls.update)


