#!/usr/bin/python3.8
from frontendclient import backendClient
tester = backendClient()
variable = {'type' : "test"}
response = tester.call(variable)
print(response)
