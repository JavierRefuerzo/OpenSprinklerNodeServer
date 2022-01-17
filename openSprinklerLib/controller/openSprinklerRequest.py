#!/usr/bin/env python3
"""
Polyglot v3 node server OpenSprinkler
Copyright (C) 2021 Javier Refuerzo

"""
from nodes.controller.drivers import ErrorValues
from objects.errors import Errors
from openSprinklerLib.controller.credenital import Credential
import requests





class OpenSprinklerRequest :

    errors: Errors = None
    jsonResponse = None
    credential: Credential

    def __init__(self, credential, endpoint, commands=[]):

        #guard
        self.credential = credential
        if self.credential == None:
            self.errors = Errors(text="Missing Credentials", code=ErrorValues.password.value)
            return
        #guard
        self.endpoint = endpoint
        if self.endpoint == None:
            self.errors = Errors(text="Missing url endpoint", code=ErrorValues.invalidUrl.value)
            return    

        params = [("pw", self.credential.password)] + commands
        url = self.credential.address + "/" + endpoint
        timeout = 30
        
        try:
            request = requests.get(url, params=params, timeout=timeout)
            print("request. url " + request.url)
            statusCode = request.status_code
            if statusCode != 200:
                self.errors = Errors(text="ConnectionError " + str(statusCode), code=statusCode)    
            self.jsonResponse = request.json()
        except Exception as e:
            self.errors = Errors(text="ConnectionError " + str(e), code=ErrorValues.connection.value)
