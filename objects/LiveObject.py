
#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""


from typing import Any, Callable, List


class LiveObject:
    
    def __init__(self, ):
        self.value: Any  = None
        self.observers: List[Callable] = []

     #------------ Attach
    def attach(self, handler: Callable):
        #if variable is not null return to handler
        if self.value != None:
            handler(self.value)
        #add handler to list            
        self.observers.append(handler)


    #------------ Remove
    def remove(self, handler):
        for handler in self.observers:
            self.observers.remove(handler)


    #------------ Notify
    
    # updates handler regardless of variable change
    def update(self, value: Any):
        self.value = value
        for handler in self.observers:
            handler(value)

    # only updates handler if variable has changed
    def updateOnChange(self, value: Any):
        #only call the handler if the value has changed
        if self.value != None and self.value == value:
            return
        self.value = value
        for handler in self.observers:
            handler(value)