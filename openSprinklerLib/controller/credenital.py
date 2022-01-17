#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""
from nodes.controller.drivers import ErrorValues
from constants.params import Params as customParms
from objects.errors import Errors
import hashlib



class Credential :
    errors: Errors = None
    password: str = None
    address: str = None

    def __init__(self, params):
        
        #Address
        self.address = params[customParms.url]
        if self.address is None or self.address == "":
            self.errors = Errors(text="Missing IP Address", code=ErrorValues.ipAddress.value)
            return

        #Password
        password = params[customParms.password]
        if password is None or password == "":
            self.errors = Errors(text="Missing Password", code=ErrorValues.password.value)
            return
        self.password = self._getPassHash(password= password)


    # -- PRIVATE Functions

    def _getPassHash(self, password: str) -> str:
        #Gaurd MD5 Password hash
        hashObject = hashlib.md5(password.encode())
        md5_hash = hashObject.hexdigest()
        if md5_hash is None:
            self.errors = Errors(text="Could not Hash Password", code=ErrorValues.password.value)
            return None
        return md5_hash