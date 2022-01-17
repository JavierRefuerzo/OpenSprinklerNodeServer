#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo
"""
import udi_interface
import sys


from nodes.controller.controller import Controller

LOGGER = udi_interface.LOGGER


# class waitingToStart():


#     def __init__(self, polyglot):
#         self.poly = polyglot
#         polyglot.subscribe(polyglot.START, self.start)


#     def start(self):
#         LOGGER.info(' start called')
#         self.poly.setCustomParamsDoc()
#         # Not necessary to call this since profile_version is used from server.json
#         self.poly.updateProfile()

#         # start processing events and create or add our controller node
#         polyglot.ready()
        
#         # Create the controller node
#         Controller(polyglot=polyglot)
       





if __name__ == "__main__":
    LOGGER.info('__name__ == "__main__" init called')
    try:
        polyglot = udi_interface.Interface([])
        polyglot.start()

        # # Create the controller node
        Controller(polyglot=polyglot)
        # waitingToStart(polyglot)

        # Just sit and wait for events
        polyglot.runForever()
    except (KeyboardInterrupt, SystemExit):
        LOGGER.info(' -JAVI - Error Occured. Most likley this is not on Polisy')
        sys.exit(0)
        


